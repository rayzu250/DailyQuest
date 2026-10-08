# Theme soundtrack and direct startup

Ten original procedural instrumental compositions are included. They use additive/FM-like
harmonic synthesis and synthesized percussion, with no external recordings, downloaded
samples, vocals, artist imitations, or music-generation services. This is a first synthesized
soundtrack for listening review, not a studio-mastered recording or a guarantee of
Content ID clearance. No third-party music license was purchased.

| Theme | Title | BPM | Duration |
| --- | --- | --- | --- |
| Forest | Senderos tranquilos | 70 | 2:17 |
| Ocean | Corrientes suaves | 64 | 2:30 |
| Sunset | Luz de la tarde | 76 | 2:06 |
| Night | Órbita serena | 62 | 2:35 |
| Prehistoric | Valle del alba | 74 | 2:10 |
| Garden | Brotes de luz | 68 | 2:21 |
| Robots | Pequeños circuitos | 80 | 2:00 |
| Mecha | Horizonte Atlas | 108 | 2:22 |
| Arcane | Páginas del cielo | 98 | 2:17 |
| Stage | Antes del escenario | 114 | 2:15 |

Primary uses gentle keys, plucked/bell-like tones, pads and sparse percussion.
Secondary uses denser bass, arpeggios and percussion. Timbres are synthesized approximations,
not recordings of guitars, orchestras or nature. Tracks contain changing arrangements,
and tails wrap into the start rather than leaving silence at the loop seam.

Files are stereo 32 kHz OGG Vorbis, about 10.5 MB total. Measured RMS is approximately
-21 dBFS across the set (not a LUFS mastering claim); decoded peaks remain below -5 dBFS.
See MUSIC_MANIFEST.json for exact duration, level, seam sample delta and SHA-256 values.
These objective checks do not replace listening on a phone.

## Playback
The normal application launch invokes Ren'Py's public Start action from label main_menu.
The first launch retains the short name onboarding. Subsequent launches restore the saved
document and open Mis tareas. No startup-menu song is played; config.main_menu_music is None.
Options remain available from the in-app menu.

All tracks loop on the existing music channel, preserving mixer preferences. Theme switches
use short fades. Re-selecting the same track uses if_changed=True to avoid restarting it.
Missing files retain the previous fallback Little_Notes_for_Big_Tasks.ogg.
Search TODO-music in game/core/music.rpy to replace tracks.

## Reproduction
tools/compose_theme_music.py uses numpy and soundfile. It refuses to overwrite existing
tracks unless --replace is passed. The development-only tools/.audio-deps directory is
ignored by Git and is not required by the game or Android build. Original code and audio
are local project outputs, with no network requirement at playback time.

## Test isolation
Ren'Py 8.5.3 also loads and writes game/saves even with --savedir. Run destructive/data-reset
tests from an isolated copy of game, excluding saves, cache and compiled scripts.
The copies used here are under tests/runtime-project (ignored by Git); their user save
directories are under tests/runtime-saves.

Run music_first_launch on a fresh isolated copy, close it, then run music_resume_launch
on that same copy and save directory. The first creates test tasks and saves a muted music
preference; the second checks direct entry, restored data, muted state, volume and real
channel track changes. Repeating the sequence requires a fresh copy and save directory.

## Desktop validation
Ren'Py 8.5.3 lint passed. Two separate launch tests passed on the same isolated
save set (first launch and subsequent launch), including persisted tasks, stage,
theme, mute and volume. The expanded_worlds suite passed all four cases, including
configured tracks and missing-file fallback. All ten OGG files decoded successfully
and passed finite-sample and clipping checks. These checks do not assess musical taste.

## Remaining device validation
No Android build was produced in this change. Listen for musical balance and loop transitions
on the phone; verify minimizing/resuming, audio interruptions, screen locking and battery
behavior on the target device. No commits or pushes were created.
