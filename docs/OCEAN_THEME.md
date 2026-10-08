# Ocean theme preview

Follow-up: Forest, Sunset and Night have now been illustrated too. See `ILLUSTRATED_THEMES.md` for the current multi-theme behavior; references below to unchanged worlds describe the initial Ocean preview.

This is a local review version. Do not commit or publish it until the owner explicitly approves.

## Assets and rendering

Generated with the built-in image generation tool (not the API/CLI fallback):

- `game/images/themes/ocean/background.png`: 941 × 1672, opaque RGB underwater scene.
- `game/images/themes/ocean/shark.png`: 1254 × 1254, RGBA guide with genuine transparency.
- `game/images/themes/ocean/button.png`: 2172 × 724, RGBA rounded sea-glass button.

Total source asset size is approximately 3.3 MiB. Original generated pixels are preserved. Ren'Py scales the background to the existing portrait canvas and adds a blue overlay for readability. The button's transparent margin is cropped at render time; a nine-slice Frame keeps its corners when controls resize. Runtime color matrices supply hover, selected and disabled states without duplicate textures. Text remains native Ren'Py text.

The ocean guide uses one welcoming pose with the existing short bounce/fade reactions. Reduced and disabled animation preferences remain supported. Additional facial expressions are not included in this preview. Other worlds keep their original backgrounds and panda assets.

Shared surfaces cover tasks, subtasks, lists, task forms, calendar, progress, theme selection, drawer, options, reminders and the text editor panel. The white editable field remains distinct from action buttons. The original launch menu and first-time introduction remain unchanged; choose Ocean through **Menú → Cambiar mundo → Océano**.

## Generation prompts

### Background

Use case: illustration-story. Create a production game background for DailyQuest, a children's task organizer ages 6–12. Portrait 9:16 underwater ocean illustration, soft rounded shapes, warm friendly hand-drawn cartoon linework, pastel turquoise and deep teal blue. Gentle light from surface at top, coral and seaweed only along the bottom corners and thin outer edges, tiny distant bubbles. Large calm uncluttertered central 75% area, medium blue with very subtle gradient so UI panels can overlay. No characters, no shark, no words, no lettering, no UI, no buttons, no watermark. Full bleed background, polished children's storybook aesthetic, no photorealism. Save generated asset for integration.

### Guide

Use case: illustration-story. Generate a NEW character sprite, using the attached red panda ONLY as style reference, do not reproduce panda. A small friendly baby shark guide for a children's task organizer. Match reference's warm cute storybook look, thick dark charcoal-purple outlines, soft cel shading, cream highlights, simple big dark eyes, rounded chunky proportions. Blue and teal shark with cream belly, full body facing viewer in a slight three-quarter view, one pectoral fin raised in a welcoming wave, little tail visible, gentle closed smile, no sharp teeth, no accessories or text. Single character centered, tightly framed occupying 85% of square canvas with all fins inside. GENUINELY TRANSPARENT background with alpha, no ocean, no shadow backdrop, no checkerboard painted in. Production PNG game sprite.

Style reference: `game/images/guias/red.png`.

### Button

Use case: stylized-concept. Production UI asset for children's ocean themed game. ONE empty rounded rectangular button, front-facing flat orthographic, width to height ratio 3:1. Aqua sea-glass body, pale mint center for dark text, thick smooth dark teal outer outline, thin turquoise inner rim, soft restrained highlight along top edge, tiny bubble engravings only at far left and right ends. Center 70% completely blank uniform pale mint. Rounded corners radius about quarter of height. Entire shape occupies nearly all width, narrow transparent margin. GENUINE TRANSPARENT alpha background outside button. No text, no letters, no icons in center, no drop shadow outside silhouette, no scenery, no multiple buttons, no perspective. Friendly hand-drawn children's cartoon style, clean scalable game control.

## Validation

Run from the project directory with the bundled Ren'Py SDK:

```powershell
& ../../lib/py3-windows-x86_64/python.exe ../../renpy.py . lint
& ../../lib/py3-windows-x86_64/python.exe ../../renpy.py . test ocean_theme --savedir tests/runtime-saves-ocean --overwrite-screenshots
```

The dedicated test changes worlds through the actual selector, checks saved theme and unchanged tasks, opens the major screens, captures large-text options, and returns to Forest and Ocean. Test data and screenshots are excluded from Git. Close the test window after its result is displayed.

Before approval on Android, check: rounded button touch targets, text at both sizes, calendar dates, scrolling through all monthly recurrence days, guide visibility/motion preferences, and theme restoration after restarting the application. No Android performance or device validation is claimed by the desktop checks.
