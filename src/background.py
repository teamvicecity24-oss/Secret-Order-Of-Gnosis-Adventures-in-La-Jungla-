"""
Background system for game levels
Supports parallax scrolling and multiple layers
"""
import pygame
import os
from src.constants import *


class BackgroundLayer:
    """Single background layer for parallax effect"""
    
    def __init__(self, image_path, scroll_speed=0.5, y_offset=0):
        """
        Args:
            image_path: Path to background image
            scroll_speed: How fast layer moves relative to camera (0.0-1.0)
            y_offset: Vertical position offset
        """
        self.scroll_speed = scroll_speed
        self.y_offset = y_offset
        
        # Load image or create fallback
        try:
            self.image = pygame.image.load(image_path).convert()
            # Scale to screen height while maintaining aspect ratio
            img_height = self.image.get_height()
            img_width = self.image.get_width()
            target_height = SCREEN_HEIGHT
            scale_factor = target_height / img_height
            new_width = int(img_width * scale_factor)
            self.image = pygame.transform.scale(self.image, (new_width, target_height))
        except:
            # Create gradient fallback
            self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            for y in range(SCREEN_HEIGHT):
                # Jungle gradient: dark green to lighter green
                color_val = int(20 + (y / SCREEN_HEIGHT) * 40)
                self.image.fill((color_val, color_val + 20, color_val), (0, y, SCREEN_WIDTH, 1))
                
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
    def draw(self, surface, camera_x):
        """Draw layer with parallax scrolling"""
        # Calculate parallax position
        parallax_x = int(camera_x * self.scroll_speed)
        
        # Calculate how many tiles needed to cover screen
        offset_x = -(parallax_x % self.width)
        
        # Draw tiled background
        x = offset_x
        while x < SCREEN_WIDTH:
            surface.blit(self.image, (x, self.y_offset))
            x += self.width


class Background:
    """Complete background with multiple parallax layers"""
    
    def __init__(self, level_number=0):
        self.layers = []
        self.level_number = level_number
        
        # Load background based on level
        self._load_background()
        
    def _load_background(self):
        """Load appropriate background for level"""
        base_path = 'assets/images/backgrounds'
        
        # Define layers for each level (back to front)
        level_backgrounds = {
            0: [  # Tutorial - simple jungle
                ('jungle_sky.png', 0.1, 0),
                ('jungle_mountains.png', 0.3, 100),
                ('jungle_trees.png', 0.5, 200),
            ],
            1: [  # Level 1 - deep jungle
                ('jungle_sky.png', 0.1, 0),
                ('jungle_ruins.png', 0.2, 50),
                ('jungle_mountains.png', 0.4, 150),
                ('jungle_trees.png', 0.6, 250),
            ],
            2: [  # Level 2 - ancient temple
                ('temple_sky.png', 0.1, 0),
                ('temple_pillars.png', 0.3, 100),
                ('temple_vines.png', 0.5, 200),
            ],
            3: [  # Level 3 - UGA's prison
                ('prison_void.png', 0.1, 0),
                ('prison_chains.png', 0.4, 100),
                ('prison_platforms.png', 0.6, 250),
            ],
        }
        
        # Get layers for this level, or default to level 0
        layer_configs = level_backgrounds.get(self.level_number, level_backgrounds[0])
        
        # Create each layer
        for filename, speed, y_offset in layer_configs:
            path = os.path.join(base_path, filename)
            layer = BackgroundLayer(path, speed, y_offset)
            self.layers.append(layer)
            
        # If no images found, create default gradient
        if not self.layers:
            self.layers.append(BackgroundLayer('', 0.3, 0))
            
    def draw(self, surface, camera_x):
        """Draw all background layers"""
        # Draw from back to front
        for layer in self.layers:
            layer.draw(surface, camera_x)
            
    def add_layer(self, image_path, scroll_speed=0.5, y_offset=0):
        """Add a new background layer"""
        layer = BackgroundLayer(image_path, scroll_speed, y_offset)
        self.layers.append(layer)


class BackgroundManager:
    """Manages backgrounds for all levels"""
    
    def __init__(self):
        self.cache = {}  # Cache backgrounds by level number
        
    def get_background(self, level_number):
        """Get or create background for a level"""
        if level_number not in self.cache:
            self.cache[level_number] = Background(level_number)
        return self.cache[level_number]
        
    def clear_cache(self):
        """Clear background cache"""
        self.cache.clear()


# README for backgrounds folder
def create_background_readme():
    """Create README for backgrounds folder"""
    readme = """# Background Images

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
"""
    return readme
