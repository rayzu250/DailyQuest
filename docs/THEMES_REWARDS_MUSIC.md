# Worlds, rewards and music

## Scope

Seven worlds are available from Menu > Change world. Prehistoric, Garden and Robots each have a new illustrated background, guide and rounded button. A scrollable selector supports larger text. Existing worlds retain their artwork.

| World | Guide | Reward |
| --- | --- | --- |
| Forest | Red panda | Acorn |
| Ocean | Shark | Fish |
| Sunset | Knight | Gem |
| Night | Astronaut | Spaceship |
| Prehistoric | Baby dinosaur | Dinosaur egg |
| Garden | Gardener | Seedling |
| Robots | Robot | Gear |

Rewards in the checklist and guide panel follow the active world. The legacy `fruit` token remains in saved documents to preserve completed steps and prevent repeat rewards. Changing worlds does not grant additional rewards. Each world currently uses one reward icon and one new guide pose with the existing motion preferences.

## Music setup

See `game/audio/themes/README.md` for the ten included theme tracks. Search `TODO-music` in `game/core/music.rpy` to change paths. World music switches on world selection, game entry and save loading. Missing files use the original track. All music respects the existing music mixer; identical tracks do not restart. See [Music and startup](MUSIC_AND_STARTUP.md) for the current soundtrack and direct startup behavior.

## Validation

Ren'Py 8.5.3 lint passed. The `expanded_worlds` suite passed four cases covering legacy theme catalogs, saved tasks, reward preservation, missing-track fallback, configured track selection, music channel flags and three visual flows. `illustrated_themes` passed three cases and `ocean_theme` passed one case. Historical tests used `--savedir tests/runtime-saves-ocean`; this alone does not isolate game/saves. Current tests use isolated game copies; see MUSIC_AND_STARTUP.md. Screenshots were reviewed for each new world, reward panels, world selector and enlarged options. All seven reward PNGs have alpha transparency. `git diff --check` passed.

These are desktop checks; this update has not been packaged or tested on Android. Validate touch scrolling, loading speed, text and audio on the phone before release. Original music remains the missing-file fallback. No commit or push was created.

## Generation details

Generated with the built-in image-generation tool. Original generated files were preserved. Project copies are listed below. Transparent button margins are cropped at runtime; the PNG files are unchanged. Reward icons and guides use real alpha transparency.

### game/images/themes/prehistoric/background.png

Prompt:

> Use case: illustration-story. DailyQuest children's task organizer ages 6–12, soft polished cartoon storybook illustration, rounded friendly shapes, gentle shading. Portrait 9:16 prehistoric valley, rounded distant volcano dormant with no lava, fern leaves and cycads along outer sides, rocky bottom corners, golden hazy sky. Calm uncluttered muted teal green central 75% for game UI, no characters. Single full bleed image. No words, labels, letters, UI or watermark. No foreground obstacles through central area.

### game/images/themes/prehistoric/guide.png

Prompt:

> Use case: illustration-story. Single full body chibi guide sprite for children's task organizer DailyQuest. Cute baby green triceratops standing upright, rounded tiny horns and orange neck frill, cream belly, smiling, one front paw waving, non-threatening. Thick warm dark purple outline, soft cel shading and cream highlights, matching polished cartoon baby shark and red panda game mascots. Centered full body occupying 85% of square canvas with ample room around all limbs. Genuine transparent alpha background, no backdrop, no floor, no text, no logos, no painted checkerboard.

### game/images/themes/prehistoric/button.png

Prompt:

> Use case: stylized-concept. ONE horizontal rounded rectangle empty button for DailyQuest children's game, aspect ratio 3:1. smooth pale sandstone slab with rounded moss green rim and tiny fossil spiral only on far ends. Wide smooth blank central 80% for dark editable text. Front facing orthographic, dark cartoon outline, soft cel shading, clean rounded corners. Genuinely transparent background outside shape, narrow margin, no external shadow, no words, letters or logos, no scenery. Single button, not a sheet.

### game/images/themes/garden/background.png

Prompt:

> Use case: illustration-story. DailyQuest children's task organizer ages 6–12, soft polished cartoon storybook illustration, rounded friendly shapes, gentle shading. Portrait 9:16 cozy planting garden, wooden raised planting beds only at bottom corners, little seedlings, flowers and watering can at outer edge, distant small greenhouse upper corner. Calm uncluttered sage green central 75% for game UI, no characters. Single full bleed image. No words, labels, letters, UI or watermark. No foreground obstacles through central area.

### game/images/themes/garden/guide.png

Prompt:

> Use case: illustration-story. Single full body chibi guide sprite for children's task organizer DailyQuest. Cute little friendly gardener girl, brown skin and dark curly hair, straw hat, green overalls with cream shirt, holding a tiny terracotta seedling pot in one hand and waving with the other. Thick warm dark purple outline, soft cel shading and cream highlights, matching polished cartoon baby shark and red panda game mascots. Centered full body occupying 85% of square canvas with ample room around all limbs. Genuine transparent alpha background, no backdrop, no floor, no text, no logos, no painted checkerboard.

### game/images/themes/garden/button.png

Prompt:

> Use case: stylized-concept. ONE horizontal rounded rectangle empty button for DailyQuest children's game, aspect ratio 3:1. pale cream plant label with rounded terracotta rim, tiny sprout carvings only on far ends. Wide smooth blank central 80% for dark editable text. Front facing orthographic, dark cartoon outline, soft cel shading, clean rounded corners. Genuinely transparent background outside shape, narrow margin, no external shadow, no words, letters or logos, no scenery. Single button, not a sheet.

### game/images/themes/robots/background.png

Prompt:

> Use case: illustration-story. DailyQuest children's task organizer ages 6–12, soft polished cartoon storybook illustration, rounded friendly shapes, gentle shading. Portrait 9:16 friendly futuristic robot workshop, rounded pastel teal and blue architecture along edges, simple distant machinery, bottom corner soft gears and cables, no robots. Calm uncluttered blue-grey central 75% for game UI. Single full bleed image. No words, labels, letters, UI or watermark. No foreground obstacles through central area.

### game/images/themes/robots/guide.png

Prompt:

> Use case: illustration-story. Single full body chibi guide sprite for children's task organizer DailyQuest. Cute small friendly robot with rounded teal body, cream face screen with expressive dark eyes and smile, orange joints, stubby rounded feet, one mitten-like mechanical hand waving. Thick warm dark purple outline, soft cel shading and cream highlights, matching polished cartoon baby shark and red panda game mascots. Centered full body occupying 85% of square canvas with ample room around all limbs. Genuine transparent alpha background, no backdrop, no floor, no text, no logos, no painted checkerboard.

### game/images/themes/robots/button.png

Prompt:

> Use case: stylized-concept. ONE horizontal rounded rectangle empty button for DailyQuest children's game, aspect ratio 3:1. pale cream metal control panel with rounded turquoise rim, small orange rivets only on far ends. Wide smooth blank central 80% for dark editable text. Front facing orthographic, dark cartoon outline, soft cel shading, clean rounded corners. Genuinely transparent background outside shape, narrow margin, no external shadow, no words, letters or logos, no scenery. Single button, not a sheet.

### game/images/themes/forest/reward.png

Prompt:

> Create a single game reward icon: a golden brown acorn with a green leaf. For DailyQuest, a friendly task game for children age 6-12. Polished hand drawn cartoon, bold dark outlines, simple chunky silhouette readable at 52 pixels, soft shading, cheerful colors. Square transparent RGBA canvas with real alpha, centered object occupies 85 percent, no text, no scenery, no border, no other objects.

### game/images/themes/ocean/reward.png

Prompt:

> Create a single game reward icon: a cute bright orange tropical fish. For DailyQuest, a friendly task game for children age 6-12. Polished hand drawn cartoon, bold dark outlines, simple chunky silhouette readable at 52 pixels, soft shading, cheerful colors. Square transparent RGBA canvas with real alpha, centered object occupies 85 percent, no text, no scenery, no border, no other objects.

### game/images/themes/sunset/reward.png

Prompt:

> Create a single game reward icon: a sparkling amber fantasy gemstone. For DailyQuest, a friendly task game for children age 6-12. Polished hand drawn cartoon, bold dark outlines, simple chunky silhouette readable at 52 pixels, soft shading, cheerful colors. Square transparent RGBA canvas with real alpha, centered object occupies 85 percent, no text, no scenery, no border, no other objects.

### game/images/themes/night/reward.png

Prompt:

> Create a single game reward icon: a small friendly blue and white spaceship. For DailyQuest, a friendly task game for children age 6-12. Polished hand drawn cartoon, bold dark outlines, simple chunky silhouette readable at 52 pixels, soft shading, cheerful colors. Square transparent RGBA canvas with real alpha, centered object occupies 85 percent, no text, no scenery, no border, no other objects.

### game/images/themes/prehistoric/reward.png

Prompt:

> Create a single game reward icon: a cream dinosaur egg with green spots. For DailyQuest, a friendly task game for children age 6-12. Polished hand drawn cartoon, bold dark outlines, simple chunky silhouette readable at 52 pixels, soft shading, cheerful colors. Square transparent RGBA canvas with real alpha, centered object occupies 85 percent, no text, no scenery, no border, no other objects.

### game/images/themes/garden/reward.png

Prompt:

> Create a single game reward icon: a bright green seedling in a terracotta pot. For DailyQuest, a friendly task game for children age 6-12. Polished hand drawn cartoon, bold dark outlines, simple chunky silhouette readable at 52 pixels, soft shading, cheerful colors. Square transparent RGBA canvas with real alpha, centered object occupies 85 percent, no text, no scenery, no border, no other objects.

### game/images/themes/robots/reward.png

Prompt:

> Create a single game reward icon: a chunky teal gear with orange center. For DailyQuest, a friendly task game for children age 6-12. Polished hand drawn cartoon, bold dark outlines, simple chunky silhouette readable at 52 pixels, soft shading, cheerful colors. Square transparent RGBA canvas with real alpha, centered object occupies 85 percent, no text, no scenery, no border, no other objects.
