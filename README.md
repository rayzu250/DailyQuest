# DailyQuest

A kid-friendly visual novel built with **Ren'Py 8.5.3** that teaches task organization
through play. Includes a full ToDo system (tasks, subtasks, lists, deadlines,
calendar, themes, progress) with a pedagogical reward loop: completing a subtask
earns a random fruit with popup animation, guide celebration and sound.

## Requirements

- Ren'Py 8.5.3 SDK, bundled locally at `renpy-8.5.3-sdk/` (untracked in git).
- Windows + VS Code (workspace tasks configured).

## Commands

- Run the game: `Ctrl+Shift+B` (task `Ren'Py: Run`), or F5 with `game/` open.
- Lint: task `Ren'Py: Lint`, or CLI `renpy-8.5.3-sdk/renpy.exe . lint`.
- Force recompile: task `Ren'Py: Force Recompile`.
- Clear persistent data: task `Ren'Py: Delete Persistent`.
- Run `Ren'Py: Lint` before committing; fix all errors and relevant warnings.

## Structure

- `game/script.rpy` — story flow, guide sprite, ATL transforms (`guia_center`,
  `reward_pop_up`, `guia_happy_bounce`, `guia_reward_bounce`).
- `game/todo_data.rpy` — data model and helpers (tasks, subtasks with per-subtask
  `deadline`/`fruit`, task-level `recurrence` rules with daily/weekly/monthly
  cycles where completing spawns the next dated copy, lists, calendar dates,
  migrations for old saves).
- `game/todo_screens.rpy` — all ToDo screens and styles, plus the `reward_popup`
  reward screen and the collapsible list dropdown.
- `game/screens.rpy`, `game/gui.rpy`, `game/options.rpy` — Ren'Py defaults,
  enlarged for the 1080x1920 portrait layout.
- `game/images/fruits/` — reward icons (`apple`, `banana`, `coconut`, `grapes`,
  `strawberry`, `watermelon`).
- `game/images/guias/` — guide sprite. `game/audio/` — music and SFX.

## Code conventions

- Indentation: 4 spaces, no tabs. Sources must be UTF-8 (mandatory on Ren'Py 8.x).
- Symbol names (labels, characters, variables, image tags, screen names) in English.
- `.rpy` organization: `define`/`init` blocks first, then labels, then screens/styles.
- Declare each character once with `define`.
- Functional comments inside the code: Spanish. In-game dialogue and copy: Spanish.

## Audio

- Format: Ogg Vorbis (`.ogg`) for all music/SFX under `game/audio/`.
- Convert `.mp3` to `.ogg` (ffmpeg not on PATH by default, use `imageio-ffmpeg`):
  `python -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())"`
  to locate the binary, then
  `& "<ffmpeg-exe>" -y -i "<input>.mp3" -c:a libvorbis -q:a 5 "<output>.ogg"`.
- If `imageio-ffmpeg` is missing: `pip install imageio-ffmpeg`.
- Verify the `.ogg` exists before deleting the source `.mp3`.

## Workflow

- Semantic commit messages (`feat:`, `fix:`, `docs:`, `refactor:`, ...).
- Feature branches only; never push directly to main.
