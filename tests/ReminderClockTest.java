import com.dailyquest.reminders.ReminderClock;
import java.util.Calendar;
import java.util.TimeZone;

public class ReminderClockTest {
    static long date(int y, int m, int d, int h, int min) {
        Calendar c = Calendar.getInstance();
        c.clear(); c.set(y, m - 1, d, h, min);
        return c.getTimeInMillis();
    }
    static void check(long actual, long expected) {
        if (actual != expected) throw new AssertionError(actual + " != " + expected);
    }
    public static void main(String[] args) {
        TimeZone.setDefault(TimeZone.getTimeZone("America/Mexico_City"));
        int[] empty = {};
        check(ReminderClock.next("", empty, 8, 30, "2026-09-24", date(2026,9,24,8,0)), date(2026,9,24,8,30));
        check(ReminderClock.next("", empty, 8, 30, "2026-09-24", date(2026,9,24,8,30)), -1);
        check(ReminderClock.next("", empty, 8, 30, "", date(2026,9,24,8,0)), -1);
        check(ReminderClock.next("diaria", empty, 8, 0, "", date(2026,9,24,8,0)), date(2026,9,25,8,0));
        check(ReminderClock.next("diaria", empty, 8, 0, "2026-10-01", date(2026,9,24,8,0)), date(2026,10,1,8,0));
        check(ReminderClock.next("semanal", new int[]{0}, 8, 0, "", date(2026,9,24,8,0)), date(2026,9,28,8,0));
        check(ReminderClock.next("semanal", empty, 8, 0, "", date(2026,9,24,8,0)), -1);
        check(ReminderClock.next("mensual", new int[]{31}, 8, 0, "", date(2028,2,1,8,0)), date(2028,2,29,8,0));
        check(ReminderClock.next("mensual", new int[]{30,31}, 8, 0, "", date(2028,2,29,8,0)), date(2028,3,30,8,0));
        check(ReminderClock.next("diaria", empty, 24, 0, "", date(2026,9,24,8,0)), -1);
        check(ReminderClock.next("", empty, 8, 0, "2026-02-30", date(2026,1,1,8,0)), -1);
        System.out.println("11 reminder clock checks passed");
    }
}
