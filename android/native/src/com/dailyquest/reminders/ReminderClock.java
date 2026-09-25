package com.dailyquest.reminders;

import java.util.Calendar;

/** Local wall-clock schedules; no dependency on Android, also tested on the JVM. */
public final class ReminderClock {
    private ReminderClock() {}

    public static long next(String frequency, int[] days, int hour, int minute,
                            String start, long after) {
        if (hour < 0 || hour > 23 || minute < 0 || minute > 59) return -1;
        Calendar first = Calendar.getInstance();
        first.setTimeInMillis(after);
        if (!start.isEmpty()) {
            try {
                String[] parts = start.split("-");
                Calendar lower = Calendar.getInstance();
                lower.clear();
                lower.setLenient(false);
                lower.set(Integer.parseInt(parts[0]), Integer.parseInt(parts[1]) - 1,
                          Integer.parseInt(parts[2]));
                if (lower.getTimeInMillis() > after || frequency.isEmpty()) first = lower;
            } catch (RuntimeException error) { return -1; }
        } else if (frequency.isEmpty()) return -1;
        for (int offset = 0; offset < 400; offset++) {
            Calendar candidate = (Calendar) first.clone();
            // Si el cambio de horario elimina esta hora, usar la siguiente hora válida.
            candidate.setLenient(true);
            candidate.add(Calendar.DATE, offset);
            candidate.set(Calendar.HOUR_OF_DAY, hour);
            candidate.set(Calendar.MINUTE, minute);
            candidate.set(Calendar.SECOND, 0);
            candidate.set(Calendar.MILLISECOND, 0);
            boolean matches = frequency.isEmpty() || frequency.equals("diaria");
            for (int day : days) {
                if (frequency.equals("semanal") && day >= 0 && day <= 6)
                    matches |= (candidate.get(Calendar.DAY_OF_WEEK) + 5) % 7 == day;
                if (frequency.equals("mensual") && day >= 1 && day <= 31)
                    matches |= candidate.get(Calendar.DAY_OF_MONTH) ==
                            Math.min(day, candidate.getActualMaximum(Calendar.DAY_OF_MONTH));
            }
            if (matches && candidate.getTimeInMillis() > after) return candidate.getTimeInMillis();
            if (frequency.isEmpty()) return -1;
        }
        return -1;
    }
}
