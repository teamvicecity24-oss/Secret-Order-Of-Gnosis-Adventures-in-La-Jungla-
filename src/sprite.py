"""
Base sprite class for all game entities
"""
import pygame
from src.constants import *


class Sprite(pygame.sprite.Sprite):
    """Base class for all game sprites with common functionality"""
    
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Velocity
        self.vel_x = 0
        self.vel_y = 0
        
        # State
        self.facing_right = True
        self.on_ground = False
        
    def update(self):
        """Update sprite position based on velocity"""
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        
    def apply_gravity(self):
        """Apply gravity to sprite"""
        if not self.on_ground:
            self.vel_y += GRAVITY
            if self.vel_y > 20:  # Terminal velocity
                self.vel_y = 20
                
    def check_collision_with_platforms(self, platforms):
        """Handle collision with platform tiles"""
        self.on_ground = False
        
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                # Check if landing on top
                if self.vel_y > 0 and self.rect.bottom <= platform.rect.centery:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                # Check if hitting from below
                elif self.vel_y < 0 and self.rect.top >= platform.rect.centery:
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0
                # Check horizontal collision
                elif self.vel_x > 0:
                    self.rect.right = platform.rect.left
                    self.vel_x = 0
                elif self.vel_x < 0:
                    self.rect.left = platform.rect.right
                    self.vel_x = 0
                    
    def move_left(self, speed):
        """Move sprite left"""
        self.vel_x = -speed
        self.facing_right = False
        
    def move_right(self, speed):
        """Move sprite right"""
        self.vel_x = speed
        self.facing_right = True
        
    def stop_horizontal(self):
        """Stop horizontal movement with friction"""
        self.vel_x = int(self.vel_x * FRICTION)
        if abs(self.vel_x) < 1:
            self.vel_x = 0
