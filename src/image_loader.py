"""
Image loading utility for game assets
"""
import pygame
import os

# Base path for assets
ASSETS_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'images')

def load_image(name, folder='characters', size=None, fallback_color=None):
    """
    Load an image from the assets folder.
    If image doesn't exist, returns a colored surface as fallback.
    
    Args:
        name: filename (e.g., 'recon_idle.png')
        folder: subfolder in assets/images
        size: (width, height) to scale to, or None for original size
        fallback_color: color tuple for fallback surface
        
    Returns:
        pygame.Surface
    """
    path = os.path.join(ASSETS_PATH, folder, name)
    
    try:
        image = pygame.image.load(path).convert_alpha()
        if size:
            image = pygame.transform.scale(image, size)
        return image
    except (pygame.error, FileNotFoundError):
        # Create fallback surface
        if size is None:
            size = (32, 48)
        surface = pygame.Surface(size, pygame.SRCALPHA)
        if fallback_color:
            surface.fill(fallback_color)
        return surface

def load_character_sprite(character_type, action='idle'):
    """
    Load a character sprite image.
    
    Args:
        character_type: one of the character constants
        action: 'idle', 'walk', 'jump', etc.
        
    Returns:
        pygame.Surface
    """
    filename = f"{character_type}_{action}.png"
    
    # Map character types to fallback colors
    color_map = {
        'recon': (0, 255, 255),      # Cyan
        'heavy': (255, 0, 0),        # Red
        'tech': (0, 0, 255),         # Blue
        'medic': (0, 255, 0),        # Green
        'stealth': (128, 0, 128),    # Purple
    }
    
    fallback_color = color_map.get(character_type, (255, 255, 255))
    return load_image(filename, 'characters', (32, 48), fallback_color)

def load_enemy_sprite(enemy_type):
    """Load an enemy sprite"""
    filename = f"{enemy_type}.png"
    
    color_map = {
        'patrol': (255, 165, 0),     # Orange
        'turret': (255, 0, 0),       # Red
        'flying': (0, 255, 255),     # Cyan
        'boss': (255, 0, 255),       # Magenta
    }
    
    fallback_color = color_map.get(enemy_type, (255, 0, 0))
    return load_image(filename, 'enemies', (32, 32), fallback_color)

def load_tile_sprite(tile_type):
    """Load a tile/platform sprite"""
    filename = f"{tile_type}.png"
    
    color_map = {
        'normal': (139, 69, 19),     # Brown
        'grass': (0, 255, 0),        # Green
        'stone': (128, 128, 128),    # Gray
        'danger': (255, 0, 0),       # Red
        'finish': (255, 0, 255),     # Magenta
    }
    
    fallback_color = color_map.get(tile_type, (139, 69, 19))
    return load_image(filename, 'tiles', (32, 32), fallback_color)

def create_placeholder_image(width, height, color, name="placeholder"):
    """Create a simple placeholder image and save it"""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    surface.fill(color)
    
    # Add a simple pattern
    pygame.draw.rect(surface, (255, 255, 255, 50), (2, 2, width-4, height-4), 1)
    
    return surface
