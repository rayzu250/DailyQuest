# Functional base rooms

Shared functionality for expedition profiles. Each existing upgrade keeps its numeric
identity and cost of three resources. No schema version change is needed: existing
world_progress records and purchases remain valid; optional rest_until is a Unix timestamp.

## Roles

| World | Upgrade 0 | Upgrade 1 | Upgrade 2 |
| --- | --- | --- | --- |
| Mecha | Planning | Library | Rest |
| Arcane | Library | Planning | Rest |
| Stage | Planning | Rest | Library |
| Additional worlds (default) | Planning | Library | Rest |

Planning filters projects by lifecycle state and priority. Project controls remain in
the existing detail screen, preserving completion checks and recurring task behavior.
Library shows completed projects and reflections. Reuse creates fresh task/step IDs,
resets progress and does not copy reminders, recurrence, dates or earned rewards.
Rest offers 5, 10 and 15 minutes, respects music preferences, and never modifies missions.
The wall-clock deadline survives suspension and document restoration. Changing the device
clock affects the countdown. No background service or Android notification is requested.
Finishing early is allowed and carries no penalty. Returning after expiry shows completion.

Three original diagram illustrations identify the rooms. Locked rooms show their purpose;
purchased rooms expose an Enter button. Normal task and history access remains available.

## Branch workflow

General is the shared release preparation branch. Personal themes belong in their own
local branch and must not be merged wholesale into General. Apply shared commits separately.
The existing main branch and remote remain unchanged until an explicit publishing request.
Build from a clean source copy when switching editions, excluding saves, cache and compiled
RenPy files, so orphaned personal scripts cannot enter a general Android build.

## Validation

RenPy lint and isolated tests cover purchasing once, preserving old unlocks, fresh IDs,
resource balances, world role mappings, profile access, and rest deadlines/restoration.
Desktop screenshots cover all three rooms. Physical Android background/resume behavior
must still be checked on device; no new APK is produced by these source changes.
