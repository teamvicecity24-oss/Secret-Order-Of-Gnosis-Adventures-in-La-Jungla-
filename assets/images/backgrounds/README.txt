# Background Images

Place background images here for parallax scrolling effects.

## File Naming Convention

Level-specific backgrounds:
- `jungle_sky.png` - Sky layer (slowest scrolling)
- `jungle_mountains.png` - Distant mountains
- `jungle_trees.png` - Foreground trees (fastest scrolling)
- `jungle_ruins.png` - Ancient ruins
- `temple_*.png` - Temple level backgrounds
- `prison_*.png` - Prison level backgrounds

## Recommended Specifications

- **Size**: 1920x1080 or larger for seamless tiling
- **Format**: PNG with transparency for layers
- **Style**: Pixel art or stylized to match game aesthetic
- **Scrolling**: Images should tile horizontally

## Parallax Setup

Each level can have multiple layers:
1. **Sky/Background** - scroll_speed: 0.1 (moves very slowly)
2. **Mountains/Ruins** - scroll_speed: 0.3 (moves slowly)
3. **Trees/Foreground** - scroll_speed: 0.5-0.6 (moves faster)

The scroll speed creates depth - distant objects move slower than nearby ones.

## Fallback

If no images are found, the game will create a gradient background automatically.

## Current Levels

- **Level 0 (Tutorial)**: Simple jungle with sky, mountains, trees
- **Level 1**: Deep jungle with ruins
- **Level 2**: Ancient temple
- **Level 3**: UGA's prison realm

Drop your images here and they will be loaded automatically!
