# Theme music

Ten original synthesized instrumental loops are included. See `docs/MUSIC_AND_STARTUP.md` and `docs/MUSIC_MANIFEST.json` for composition details and measurements.

| Context | Filename |
| --- | --- |
| Forest | `forest.ogg` |
| Ocean | `ocean.ogg` |
| Sunset | `sunset.ogg` |
| Night / space | `night.ogg` |
| Prehistoric | `prehistoric.ogg` |
| Garden | `garden.ogg` |
| Robots | `robots.ogg` |
| Secondary: Mecha | `secondary/mecha.ogg` |
| Secondary: Arcane | `secondary/arcane.ogg` |
| Secondary: Stage | `secondary/stage.ogg` |

You can replace these OGG files after listening review. Missing tracks fall back to `audio/Little_Notes_for_Big_Tasks.ogg`. To use other names, edit `game/core/music.rpy` at `TODO-music`.

Theme music loops on the existing music channel and respects the music volume. Switching worlds fades between different tracks; the same track continues without restarting. The application now starts directly, so no separate main-menu track is needed. Test a new Android build after replacing tracks.
