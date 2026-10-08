# Illustrated world themes

Local review changes only. No commit or upload is authorized yet.

All four worlds now use illustrated backgrounds, scalable rounded buttons and matching panel colors. Forest preserves the existing panda sprites and expressions. Sunset uses a welcoming knight, Night an astronaut and Ocean the existing shark. New guides each have one pose and reuse the existing bounce/fade reactions; no continuous animation is added. Reduced/off motion preferences are preserved.

The assets were generated using the built-in image generation tool, not the API/CLI fallback. Original PNGs are preserved. Button margins are cropped at render time and a nine-slice Frame adapts the control without stretching its corners. Hover, selection and disabled appearances use color matrices. Text stays editable in Ren'Py.

## Saved assets and generation prompts

### forest: background

Saved to `game/images/themes/forest/background.png`.

Use case: illustration-story. Production background for DailyQuest children's task organizer ages 6–12, consistent soft storybook cartoon illustration, rounded shapes and subtle painterly shading. Portrait 9:16 peaceful forest clearing, layered rounded green trees at sides, soft sunlight through canopy, tiny ferns and flowers in bottom corners. Deep sage green uncluttered central 75%. Full bleed. Central area kept calm for readable overlaid task panels. No characters, no words, no lettering, no UI, no watermark, no buttons. Polished friendly illustration matching an underwater cartoon game theme. Output a single portrait background.

### forest: button

Saved to `game/images/themes/forest/button.png`.

Use case: stylized-concept. ONE production UI button image for a children's game. A light honey wood plaque with smooth sage-green rim and tiny carved leaf details at the far ends; cream pale wood center. Horizontal rounded rectangle, width to height 3:1, front view orthographic, no perspective. Thick clean dark outline, gentle cel shading, softly beveled edges. All decorations confined to outer ends, central 75% completely blank and smooth for editable dark text. Genuinely transparent alpha background outside silhouette, narrow transparent margins. No text, no letters, no words, no logos, no scenery, no external shadow, no multiple buttons. Match soft polished storybook cartoon style. Rounded corners remain clear.

### sunset: background

Saved to `game/images/themes/sunset/background.png`.

Use case: illustration-story. Production background for DailyQuest children's task organizer ages 6–12, consistent soft storybook cartoon illustration, rounded shapes and subtle painterly shading. Portrait 9:16 sunset hills with a tiny friendly fairytale castle far away near outer upper right edge, peach and muted gold sky, terracotta hills framing edges and bottom corners. Muted warm plum uncluttered central 75%. Full bleed. Central area kept calm for readable overlaid task panels. No characters, no words, no lettering, no UI, no watermark, no buttons. Polished friendly illustration matching an underwater cartoon game theme. Output a single portrait background.

### sunset: button

Saved to `game/images/themes/sunset/button.png`.

Use case: stylized-concept. ONE production UI button image for a children's game. A warm ivory medieval plaque with rounded golden metal rim and small copper rivets only at the far ends; pale peach cream center. Horizontal rounded rectangle, width to height 3:1, front view orthographic, no perspective. Thick clean dark outline, gentle cel shading, softly beveled edges. All decorations confined to outer ends, central 75% completely blank and smooth for editable dark text. Genuinely transparent alpha background outside silhouette, narrow transparent margins. No text, no letters, no words, no logos, no scenery, no external shadow, no multiple buttons. Match soft polished storybook cartoon style. Rounded corners remain clear.

### sunset: guide

Saved to `game/images/themes/sunset/guide.png`.

Use case: illustration-story. Single full-body children's game guide sprite for DailyQuest ages 6–12. Friendly small storybook knight guide, rounded silver armor with warm gold trim, short peach cape, open helmet showing a smiling friendly face with big dark eyes. One mitten-like gauntlet raised waving. No weapon, no shield, no emblems. Cute chibi proportions, warm thick dark purple outline, soft cel shading, cream highlights, consistent style with a welcoming cartoon red panda and baby shark. Center character occupying 85% of square canvas, all limbs inside, genuinely transparent alpha background. No scenery, no text, no painted checkerboard, no ground shadow. Polished 2D cartoon game PNG.

### night: background

Saved to `game/images/themes/night/background.png`.

Use case: illustration-story. Production background for DailyQuest children's task organizer ages 6–12, consistent soft storybook cartoon illustration, rounded shapes and subtle painterly shading. Portrait 9:16 peaceful outer space, deep indigo navy, soft stars sparsely placed mostly at edges, crescent planet at upper corner, small pastel planets at lower corners. Dark calm uncluttered central 75%. Full bleed. Central area kept calm for readable overlaid task panels. No characters, no words, no lettering, no UI, no watermark, no buttons. Polished friendly illustration matching an underwater cartoon game theme. Output a single portrait background.

### night: button

Saved to `game/images/themes/night/button.png`.

Use case: stylized-concept. ONE production UI button image for a children's game. A friendly futuristic space panel with rounded indigo rim and small lavender indicator lights only at the far ends; pale lavender cream center. Horizontal rounded rectangle, width to height 3:1, front view orthographic, no perspective. Thick clean dark outline, gentle cel shading, softly beveled edges. All decorations confined to outer ends, central 75% completely blank and smooth for editable dark text. Genuinely transparent alpha background outside silhouette, narrow transparent margins. No text, no letters, no words, no logos, no scenery, no external shadow, no multiple buttons. Match soft polished storybook cartoon style. Rounded corners remain clear.

### night: guide

Saved to `game/images/themes/night/guide.png`.

Use case: illustration-story. Single full-body children's game guide sprite for DailyQuest ages 6–12. Friendly small astronaut guide in a rounded cream space suit with lavender and blue details, oversized round helmet with transparent visor revealing a smiling friendly face and big dark eyes, one gloved hand raised waving. Small rounded boots and backpack. No flags, no logos. Cute chibi proportions, warm thick dark purple outline, soft cel shading, cream highlights, consistent style with a welcoming cartoon red panda and baby shark. Center character occupying 85% of square canvas, all limbs inside, genuinely transparent alpha background. No scenery, no text, no painted checkerboard, no ground shadow. Polished 2D cartoon game PNG.

## Validation

Run `lint` and the `illustrated_themes` suite with the bundled Ren'Py SDK and `--savedir tests/runtime-saves-ocean --overwrite-screenshots`. The suite switches through the real world selector, verifies task preservation and theme persistence, captures tasks, help, menu, calendar, large-text options and subtasks, and returns to Ocean after each world.

Desktop screenshots are stored in `tests/screenshots/` and excluded from Git. Android touch targets, memory use and appearance on the physical phone still require device validation. No APK is produced by these visual changes. The standard Ren'Py launch menu and first-time introduction remain unchanged.
