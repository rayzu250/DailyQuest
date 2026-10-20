# Reminder editor feedback

The reported Android symptom is an editor that remains open after saving even when
the user sees a date or recurrence. This exact device case has not been reproduced.
The inspected APK contains the native Reminders class and setTheme method.

A confirmed independent defect was found: notify used zorder 100 underneath the
opaque reminder editor at 140, hiding validation errors. Notifications now use 300.
The editor displays persistent validation feedback, the actual task date and recurrence,
and allows selecting the task date directly. The calendar uses zorder 150 to appear
above the editor. Subtask dates remain separate; no date is inferred or silently changed.
Successful saves explicitly report that the time was saved, followed by permission status.

Three isolated desktop reminder cases passed, covering recurrence, persistence,
editor save/cancel, subtask-only date rejection, visible validation and saving with a
task date. Ren'Py lint passed and a validation screenshot was reviewed. No Android
APK was generated for this fix; delivery and the original phone symptom remain to
be verified. No commit or push was created.
