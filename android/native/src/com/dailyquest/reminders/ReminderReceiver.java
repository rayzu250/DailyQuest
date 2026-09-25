package com.dailyquest.reminders;
import android.content.*;

public final class ReminderReceiver extends BroadcastReceiver {
    @Override public void onReceive(Context context, Intent intent) {
        if (intent.getData() != null && "dailyquest".equals(intent.getData().getScheme()))
            Reminders.fire(context, intent);
        else Reminders.reschedule(context);
    }
}
