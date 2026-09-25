package com.dailyquest.reminders;

import android.Manifest;
import android.app.*;
import android.content.*;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Build;
import android.provider.Settings;
import org.json.*;

/** All state needed while Python is stopped lives in private SharedPreferences. */
public final class Reminders {
    private static final String CHANNEL = "dailyquest_tasks_v1";
    private static final String PREFS = "dailyquest_reminders";
    private Reminders() {}
    private static SharedPreferences prefs(Context c) {
        return c.getSharedPreferences(PREFS, Context.MODE_PRIVATE);
    }
    private static NotificationManager notifications(Context c) {
        return (NotificationManager)c.getSystemService(Context.NOTIFICATION_SERVICE);
    }
    private static AlarmManager alarms(Context c) {
        return (AlarmManager)c.getSystemService(Context.ALARM_SERVICE);
    }
    private static JSONArray data(Context c) {
        try { return new JSONArray(prefs(c).getString("tasks", "[]")); }
        catch (JSONException error) { return new JSONArray(); }
    }
    public static void channel(Context c) {
        if (Build.VERSION.SDK_INT >= 26) {
            NotificationChannel channel = new NotificationChannel(CHANNEL,
                    "Recordatorios de tareas", NotificationManager.IMPORTANCE_DEFAULT);
            channel.setDescription("Avisos de las tareas que elegiste recordar.");
            channel.setLockscreenVisibility(Notification.VISIBILITY_PRIVATE);
            notifications(c).createNotificationChannel(channel);
        }
    }
    public static boolean allowed(Context c) {
        channel(c);
        if (Build.VERSION.SDK_INT >= 33 && c.checkSelfPermission(Manifest.permission.POST_NOTIFICATIONS)
                != PackageManager.PERMISSION_GRANTED) return false;
        if (Build.VERSION.SDK_INT >= 24 && !notifications(c).areNotificationsEnabled()) return false;
        return Build.VERSION.SDK_INT < 26 || notifications(c).getNotificationChannel(CHANNEL)
                .getImportance() != NotificationManager.IMPORTANCE_NONE;
    }
    public static boolean exact(Context c) {
        return Build.VERSION.SDK_INT < 31 || alarms(c).canScheduleExactAlarms();
    }
    private static PendingIntent alarmIntent(Context c, String id, long when) {
        Intent intent = new Intent(c, ReminderReceiver.class);
        intent.setData(Uri.parse("dailyquest://alarm/" + id));
        intent.putExtra("id", id);
        intent.putExtra("when", when);
        return PendingIntent.getBroadcast(c, 0, intent,
                PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
    }
    private static void cancel(Context c, String id) {
        alarms(c).cancel(alarmIntent(c, id, 0));
        notifications(c).cancel(id, 1);
        prefs(c).edit().remove("scheduled_" + id).remove("spec_" + id)
                .remove("exact_" + id).commit();
    }
    private static void schedule(Context c, JSONObject task, boolean force) throws JSONException {
        String id = task.getString("id");
        long pending = prefs(c).getLong("scheduled_" + id, 0);
        boolean precise = exact(c);
        // Un guardado ajeno a este horario no debe cancelar un aviso aproximado retrasado.
        if (!force && pending > 0 && allowed(c)
                && task.toString().equals(prefs(c).getString("spec_" + id, ""))
                && precise == prefs(c).getBoolean("exact_" + id, false)) return;
        JSONArray rawDays = task.optJSONArray("days");
        int[] days = new int[rawDays == null ? 0 : rawDays.length()];
        for (int i = 0; i < days.length; i++) days[i] = rawDays.getInt(i);
        long after = Math.max(System.currentTimeMillis(), prefs(c).getLong("fired_" + id, 0));
        long when = ReminderClock.next(task.optString("freq"), days, task.getInt("hour"),
                task.getInt("minute"), task.optString("start"), after);
        alarms(c).cancel(alarmIntent(c, id, 0));
        prefs(c).edit().remove("scheduled_" + id).commit();
        if (when < 0 || !allowed(c)) return;
        PendingIntent intent = alarmIntent(c, id, when);
        prefs(c).edit().putLong("scheduled_" + id, when)
                .putString("spec_" + id, task.toString()).putBoolean("exact_" + id, precise).commit();
        if (precise) {
            try {
                if (Build.VERSION.SDK_INT >= 23)
                    alarms(c).setExactAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, when, intent);
                else alarms(c).setExact(AlarmManager.RTC_WAKEUP, when, intent);
                return;
            } catch (SecurityException permissionRevoked) { /* Fall back without losing the task. */ }
        }
        if (Build.VERSION.SDK_INT >= 23)
            alarms(c).setAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, when, intent);
        else alarms(c).set(AlarmManager.RTC_WAKEUP, when, intent);
    }
    public static synchronized void sync(Context c, String json) throws JSONException {
        JSONArray next = new JSONArray(json);
        JSONArray old = data(c);
        for (int i = 0; i < old.length(); i++) {
            JSONObject previous = old.getJSONObject(i);
            boolean exists = false;
            for (int j = 0; j < next.length(); j++)
                if (previous.getString("id").equals(next.getJSONObject(j).getString("id"))) {
                    exists = true;
                    if (!previous.toString().equals(next.getJSONObject(j).toString()))
                        cancel(c, previous.getString("id"));
                }
            if (!exists) {
                cancel(c, previous.getString("id"));
                prefs(c).edit().remove("fired_" + previous.getString("id")).commit();
            }
        }
        if (!prefs(c).edit().putString("tasks", json).commit())
            throw new IllegalStateException("Cannot save reminder schedule");
        for (int i = 0; i < next.length(); i++) schedule(c, next.getJSONObject(i), false);
    }
    public static synchronized void reschedule(Context c) {
        JSONArray tasks = data(c);
        for (int i = 0; i < tasks.length(); i++) {
            try { schedule(c, tasks.getJSONObject(i), true); }
            catch (JSONException error) { android.util.Log.e("DailyQuest", "Invalid reminder", error); }
        }
    }
    static synchronized void fire(Context c, Intent intent) {
        String id = intent.getStringExtra("id");
        long when = intent.getLongExtra("when", 0);
        if (id == null || when <= prefs(c).getLong("fired_" + id, 0)) return;
        if (when != prefs(c).getLong("scheduled_" + id, 0)) return;
        JSONArray tasks = data(c);
        for (int i = 0; i < tasks.length(); i++) {
            try {
                JSONObject task = tasks.getJSONObject(i);
                if (!id.equals(task.getString("id"))) continue;
                // Save before posting: avoid duplicate alarms after restarting the process.
                prefs(c).edit().putLong("fired_" + id, when).remove("scheduled_" + id).commit();
                if (allowed(c)) {
                    Intent open = new Intent(c, ReminderOpenActivity.class);
                    open.setData(Uri.parse("dailyquest://task/" + id));
                    open.putExtra("id", id);
                    PendingIntent tap = PendingIntent.getActivity(c, 0, open,
                            PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
                    Notification.Builder builder = Build.VERSION.SDK_INT >= 26 ?
                            new Notification.Builder(c, CHANNEL) : new Notification.Builder(c);
                    int icon = c.getResources().getIdentifier("ic_quest_reminder", "drawable", c.getPackageName());
                    builder.setSmallIcon(icon).setContentTitle("Un paso para tu día")
                            .setContentText(task.getString("title"))
                            .setStyle(new Notification.BigTextStyle().bigText(task.getString("title")))
                            .setContentIntent(tap).setAutoCancel(true).setOnlyAlertOnce(true)
                            .setVisibility(Notification.VISIBILITY_PRIVATE)
                            .setCategory(Notification.CATEGORY_REMINDER);
                    if (Build.VERSION.SDK_INT < 26) builder.setDefaults(Notification.DEFAULT_ALL);
                    notifications(c).notify(id, 1, builder.build());
                }
                schedule(c, task, true);
                return;
            } catch (JSONException error) { android.util.Log.e("DailyQuest", "Invalid reminder", error); }
        }
    }
    static void openTask(Context c, String id) {
        prefs(c).edit().putString("open_task", id).commit();
    }
    public static synchronized String consumeTask(Context c) {
        String id = prefs(c).getString("open_task", "");
        prefs(c).edit().remove("open_task").commit();
        return id;
    }
    public static void notificationSettings(Activity a) {
        Intent intent = new Intent(Build.VERSION.SDK_INT >= 26 ?
                Settings.ACTION_CHANNEL_NOTIFICATION_SETTINGS : Settings.ACTION_APPLICATION_DETAILS_SETTINGS);
        if (Build.VERSION.SDK_INT >= 26) {
            intent.putExtra(Settings.EXTRA_APP_PACKAGE, a.getPackageName());
            intent.putExtra(Settings.EXTRA_CHANNEL_ID, CHANNEL);
        } else intent.setData(Uri.parse("package:" + a.getPackageName()));
        a.startActivity(intent);
    }
    public static void exactSettings(Activity a) {
        if (Build.VERSION.SDK_INT >= 31)
            a.startActivity(new Intent(Settings.ACTION_REQUEST_SCHEDULE_EXACT_ALARM,
                    Uri.parse("package:" + a.getPackageName())));
    }
}
