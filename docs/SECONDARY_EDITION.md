# Secondary school edition

## Access and scope
Select **Opciones > Secundaria · 12 a 15 años**. Primary retains its seven worlds. Secondary has Escuadrón Mecha, Academia Arcana and Camino al Escenario, with original backgrounds, guide sprites, rounded buttons and reward icons. Each stage remembers its last theme.

This delivery implements a first playable expedition system across those three worlds:
- Start, pause, resume, finish and reopen missions.
- Choose a mission world and one of three named color variants before starting.
- A departure/return scene that respects normal, reduced and disabled motion.
- A four-card-per-page mission overview, completed history and resource panel.
- One resource per newly completed step; three resources unlock a base improvement.
- Goal, optional reflection and priority; upcoming seven-day filter; existing lists can represent subjects.
- Menu and onboarding visuals follow the current world.
- Existing Android reminder behavior is reused.

## Data and safeguards
Document version 2 accepts version 1 saves and adds stage, remembered themes and world progress. A mission owns its world independently of the current UI theme. Earned step IDs prevent duplicated resources when reopening steps, missions or saved data. Existing completed steps keep their rewards and do not retroactively generate inventory. Primary mode hides advanced controls without deleting expedition data. Switching stage from the startup menu restores existing data before saving; fresh users are not given an empty document that skips onboarding.

Recurring missions create a fresh planned expedition in the same world with uncompleted steps. A completed expedition must be reopened before editing its checklist. Resource unlocks are persistent, with no absence penalties.

## Current visual limits and next work
Characters currently have one full-body illustration per world, three tint/name variants, and short position/fade animations. The overview is a paginated card map rather than a freely navigable scene. Base improvements currently unlock named entries in the base panel; they do not yet rebuild the background. A broader collectible resource set, distinct character illustrations, visible building upgrades, and the later island/magic-colony expansions remain subsequent roadmap work.

No Android APK has been built or tested for this delivery. Validate phone performance, touch scrolling, enlarged fonts, reminders and audio before release. No commits or pushes were created.

## Validation

Ren'Py 8.5.3 desktop test results: secondary (6 cases), quest (2), options_guide (3), expanded_worlds (4): all 15 passed. Checks cover version-1 migration, independent theme memory, startup stage changes without data loss, empty-document onboarding, mission lifecycle, recurrence, resource deduplication, saving/reloading, primary task workflows, music fallback and accessibility options. Screenshots of all three secondary worlds, planning, departure/return, resource panels, history, card overview and enlarged options were reviewed. Final lint passed; no whitespace errors were reported by git diff --check.

## Music files
Search `TODO-music` in `game/core/music.rpy`.
Add:
- `game/audio/themes/secondary/mecha.ogg`
- `game/audio/themes/secondary/arcane.ogg`
- `game/audio/themes/secondary/stage.ogg`

All three secondary tracks are now included. Absent files use the existing fallback song. Startup now opens the application directly without main-menu music. See [Music and startup](MUSIC_AND_STARTUP.md).

## Assets
Built-in image generation was used; no API/CLI fallback. Original generated images were preserved. Project copies:
- `game/images/themes/mecha/{background,guide,button,reward}.png`
- `game/images/themes/arcane/{background,guide,button,reward}.png`
- `game/images/themes/stage/{background,guide,button,reward}.png`

Buttons are cropped at runtime; the original PNGs are unchanged. The first decorative button proposals were rejected in favor of simpler blank interiors.

### Final prompt set
Backgrounds, guides and resources used this common prefix:
> Use case: stylized-concept. Asset for DailyQuest secondary school edition ages 12-15. Polished contemporary anime game illustration, elegant confident silhouettes, restrained detail, soft cinematic shading, not chibi, not baby proportions, no text or watermark.

Subjects appended:
- Mecha background: Portrait 9:16 futuristic hangar opening toward a distant city at dawn, docking structures along outer edges, navy steel and cyan lighting, quiet broad central floor for overlay UI. No characters.
- Arcane background: Portrait 9:16 grand arcane academy library with tall arches, violet twilight and subtle gold runes along edges, distant floating observatory, quiet uncluttered central space for overlay UI. No characters.
- Stage background: Portrait 9:16 contemporary music rehearsal studio opening onto an empty concert stage, indigo teal magenta lighting, instruments along outer edges, quiet uncluttered center for overlay UI. No characters, no crowd.
- Mecha guide: Single original heroic full body humanoid giant mecha, streamlined ivory navy cyan armor, asymmetric shoulder shield, sleek single visor, no weapons, confident relaxed stance. Distinct original design, no logos or franchise emblems. Transparent RGBA background, square canvas, full body uncropped.
- Arcane guide: Single original adolescent wizard apprentice age 15, fully clothed in practical layered navy and violet academy robes, short dark hair, holding closed luminous gold grimoire, calm confident stance, full body. Transparent RGBA background, square canvas, uncropped.
- Stage guide: Single original adolescent singer age 15, fully clothed in contemporary teal jacket, indigo trousers and sneakers, holding a microphone, relaxed confident stance, short wavy hair, full body, no celebrity likeness. Transparent RGBA background, square canvas, uncropped.
- Mecha reward: Single compact futuristic cyan energy core in navy metal housing, inventory resource icon, square transparent RGBA canvas, fills 85 percent, legible at 52 pixels, no words.
- Arcane reward: Single violet faceted runestone wrapped in a simple gold band, inventory resource icon, square transparent RGBA canvas, fills 85 percent, legible at 52 pixels, no words.
- Stage reward: Single stylized teal musical note with indigo and magenta accent, inventory resource icon, square transparent RGBA canvas, fills 85 percent, legible at 52 pixels, no words.

Final buttons used:
> Use case: ui-mockup. A SINGLE EMPTY UI BUTTON ASSET ONLY. Wide 3:1 canvas. Rounded rectangular blank ivory button with [design]. Flat professional minimal game interface for teenagers. Extremely thin border occupies less than 5% of button width. Entire interior blank uniform pale ivory for dark text. Genuine transparent alpha outside the rounded rectangle. NO PEOPLE, NO FACES, NO CHARACTERS, NO ANIMALS, NO OBJECTS, NO FLOWERS, NO SCENERY, NO LETTERS, NO TEXT, NO LOGOS. Nothing besides one simple empty rounded rectangle.

Design substitutions: Mecha = navy metal rim with a cyan edge; Arcane = dark violet rim with a thin gold edge; Stage = indigo rim with teal and magenta edge lights.
