"""
Weapon and bullet classes
"""
import pygame
from src.constants import *


class Bullet(pygame.sprite.Sprite):
    """Bullet projectile"""
    
    def __init__(self, x, y, direction, damage, explosive=False, speed=BULLET_SPEED):
        super().__init__()
        self.damage = damage
        self.direction = direction
        self.explosive = explosive
        self.speed = speed
        
        size = 8 if not explosive else 16
        self.image = pygame.Surface([size, size])
        color = YELLOW if not explosive else ORANGE
        self.image.fill(color)
        
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
    def update(self):
        """Move bullet"""
        self.rect.x += self.speed * self.direction
        
        # Remove if off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
            
    def draw(self, surface, camera_x=0):
        """Draw bullet"""
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y))


class Explosion(pygame.sprite.Sprite):
    """Explosion effect for explosive bullets"""
    
    def __init__(self, x, y, radius=60, damage=30):
        super().__init__()
        self.x = x
        self.y = y
        self.radius = radius
        self.damage = damage
        self.max_lifetime = 20
        self.lifetime = self.max_lifetime
        
    def update(self):
        """Update explosion"""
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()
            
    def draw(self, surface, camera_x=0):
        """Draw explosion"""
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        radius = int(self.radius * (2 - self.lifetime / self.max_lifetime))
        
        explosion_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(explosion_surface, (255, 100, 0, alpha), (radius, radius), radius)
        pygame.draw.circle(explosion_surface, (255, 200, 0, alpha), (radius, radius), radius * 0.7)
        surface.blit(explosion_surface, (self.x - radius - camera_x, self.y - radius))
