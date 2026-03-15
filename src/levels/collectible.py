"""
Collectible items (coins, keys, power-ups)
"""
import pygame
from src.constants import *


class Collectible(pygame.sprite.Sprite):
    """Base collectible class"""
    
    def __init__(self, x, y, size, color, value=0):
        super().__init__()
        self.image = pygame.Surface([size, size])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.value = value
        self.bob_offset = 0
        self.bob_speed = 0.1
        
    def update(self):
        """Animate collectible bobbing"""
        self.bob_offset += self.bob_speed
        
    def draw(self, surface, camera_x=0):
        """Draw collectible with bob animation"""
        y_offset = int(5 * pygame.math.Vector2(1, 0).rotate(self.bob_offset * 50).y)
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y + y_offset))


class Coin(Collectible):
    """Score coin"""
    
    def __init__(self, x, y):
        super().__init__(x + 8, y + 8, 16, YELLOW, 100)
        # Make it circular
        self.image.fill(BLACK)
        pygame.draw.circle(self.image, YELLOW, (8, 8), 7)
        pygame.draw.circle(self.image, WHITE, (8, 8), 4)


class Key(Collectible):
    """Key for unlocking doors/puzzles"""
    
    def __init__(self, x, y, key_id=1):
        super().__init__(x + 4, y + 4, 24, BLUE, 500)
        self.key_id = key_id
        # Draw key shape
        self.image.fill(BLACK)
        pygame.draw.circle(self.image, BLUE, (12, 8), 6)
        pygame.draw.rect(self.image, BLUE, (10, 12, 4, 12))
        pygame.draw.rect(self.image, BLUE, (14, 16, 4, 4))


class HealthPack(Collectible):
    """Health restoration item"""
    
    def __init__(self, x, y, amount=25):
        super().__init__(x + 4, y + 4, 24, RED, 0)
        self.heal_amount = amount
        # Draw health cross
        self.image.fill(BLACK)
        pygame.draw.rect(self.image, RED, (4, 8, 16, 8))
        pygame.draw.rect(self.image, RED, (8, 4, 8, 16))
        pygame.draw.rect(self.image, WHITE, (6, 10, 12, 4))
        pygame.draw.rect(self.image, WHITE, (10, 6, 4, 12))


class AmmoPack(Collectible):
    """Ammo/power-up for special abilities"""
    
    def __init__(self, x, y):
        super().__init__(x + 4, y + 4, 24, ORANGE, 0)
        # Draw ammo box
        self.image.fill(BLACK)
        pygame.draw.rect(self.image, ORANGE, (2, 4, 20, 16))
        pygame.draw.rect(self.image, YELLOW, (6, 8, 12, 8))
