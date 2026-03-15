"""
Player base class and 5 unique character classes
"""
import pygame
from src.constants import *
from src.sprite import Sprite
from src.weapons.bullet import Bullet
from src.image_loader import load_character_sprite


class Player(Sprite):
    """Base player class with common functionality"""
    
    def __init__(self, x, y, character_type):
        self.character_type = character_type
        
        # Load character image
        self.image = load_character_sprite(character_type, 'idle')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Character attributes (override in subclasses)
        self.max_health = PLAYER_MAX_HEALTH
        self.health = self.max_health
        self.speed = PLAYER_SPEED
        self.jump_strength = PLAYER_JUMP_STRENGTH
        self.shoot_cooldown = BULLET_COOLDOWN
        
        # Special ability
        self.special_name = "None"
        self.special_cooldown = 5000
        self.special_timer = 0
        
        # Shooting
        self.last_shot = 0
        self.bullets = pygame.sprite.Group()
        
        # Invincibility after damage
        self.invincible = False
        self.invincible_timer = 0
        
        # Animation
        self.anim_frame = 0
        self.anim_timer = 0
        
    def update(self, platforms, enemies, all_sprites, current_time):
        """Update player state"""
        super().update()
        self.apply_gravity()
        self.check_collision_with_platforms(platforms)
        
        # Apply friction when on ground
        if self.on_ground:
            self.stop_horizontal()
        else:
            self.vel_x = int(self.vel_x * AIR_RESISTANCE)
            
        # Update invincibility
        if self.invincible and current_time - self.invincible_timer > PLAYER_INVINCIBILITY_TIME:
            self.invincible = False
            
        # Update special ability cooldown
        if self.special_timer > 0 and current_time - self.special_timer > self.special_cooldown:
            self.special_timer = 0
            
        # Keep player in bounds
        if self.rect.left < 0:
            self.rect.left = 0
            self.vel_x = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.vel_x = 0
        if self.rect.top > SCREEN_HEIGHT:
            self.health = 0  # Fall death
            
        # Update bullets
        self.bullets.update()
        
        # Check bullet collisions with enemies
        for bullet in self.bullets:
            hit_enemies = pygame.sprite.spritecollide(bullet, enemies, False)
            for enemy in hit_enemies:
                enemy.take_damage(bullet.damage)
                bullet.kill()
                break
                
    def jump(self):
        """Make player jump if on ground"""
        if self.on_ground:
            self.vel_y = -self.jump_strength
            self.on_ground = False
            
    def shoot(self, current_time):
        """Fire a bullet"""
        if current_time - self.last_shot > self.shoot_cooldown:
            self.last_shot = current_time
            direction = 1 if self.facing_right else -1
            bullet = Bullet(
                self.rect.centerx,
                self.rect.centery,
                direction,
                self.get_bullet_damage()
            )
            self.bullets.add(bullet)
            return bullet
        return None
        
    def get_bullet_damage(self):
        """Override in subclasses for different damage values"""
        return 10
        
    def use_special(self, current_time):
        """Use special ability - override in subclasses"""
        if self.special_timer == 0:
            self.special_timer = current_time
            return self._activate_special()
        return None
        
    def _activate_special(self):
        """Override this in subclasses for special ability effects"""
        pass
        
    def take_damage(self, amount, current_time):
        """Take damage with invincibility frames"""
        if not self.invincible:
            self.health -= amount
            self.invincible = True
            self.invincible_timer = current_time
            # Knockback
            self.vel_y = -5
            self.vel_x = -10 if self.facing_right else 10
            
    def heal(self, amount):
        """Heal the player"""
        self.health = min(self.health + amount, self.max_health)
        
    def is_alive(self):
        """Check if player is alive"""
        return self.health > 0
        
    def draw(self, surface, camera_x=0):
        """Draw player and bullets"""
        # Draw bullets
        for bullet in self.bullets:
            bullet.draw(surface, camera_x)
            
        # Draw player with invincibility blink
        if not self.invincible or pygame.time.get_ticks() % 200 < 100:
            surface.blit(self.image, (self.rect.x - camera_x, self.rect.y))
            
        # Draw health bar
        bar_width = 32
        bar_height = 4
        health_pct = self.health / self.max_health
        pygame.draw.rect(surface, RED, (self.rect.x - camera_x, self.rect.y - 10, bar_width, bar_height))
        pygame.draw.rect(surface, GREEN, (self.rect.x - camera_x, self.rect.y - 10, bar_width * health_pct, bar_height))


class Recon(Player):
    """Recon - Fast scout with rapid fire and speed boost"""
    
    def __init__(self, x, y):
        super().__init__(x, y, CHARACTER_RECON)
        # Image loaded from assets/images/characters/recon_idle.png
        self.speed = PLAYER_SPEED + 3
        self.max_health = PLAYER_MAX_HEALTH - 20
        self.health = self.max_health
        self.shoot_cooldown = BULLET_COOLDOWN - 100
        self.special_name = "Speed Boost"
        self.special_cooldown = 8000
        self.speed_boost_active = False
        self.normal_speed = self.speed
        
    def get_bullet_damage(self):
        return 8
        
    def _activate_special(self):
        """Speed boost - doubles speed temporarily"""
        self.speed_boost_active = True
        self.speed = self.normal_speed * 2
        self.shoot_cooldown = 50  # Super fast firing
        return "Speed Boost Activated!"
        
    def update(self, platforms, enemies, all_sprites, current_time):
        super().update(platforms, enemies, all_sprites, current_time)
        # Deactivate speed boost after 3 seconds
        if self.speed_boost_active and current_time - self.special_timer > 3000:
            self.speed_boost_active = False
            self.speed = self.normal_speed
            self.shoot_cooldown = BULLET_COOLDOWN - 100


class Heavy(Player):
    """Heavy - Slow tank with high health and explosive shots"""
    
    def __init__(self, x, y):
        super().__init__(x, y, CHARACTER_HEAVY)
        # Image loaded from assets/images/characters/heavy_idle.png
        self.rect.height = 56
        self.image = load_character_sprite(CHARACTER_HEAVY, 'idle')
        self.image = pygame.transform.scale(self.image, (32, 56))
        self.speed = PLAYER_SPEED - 2
        self.max_health = PLAYER_MAX_HEALTH + 50
        self.health = self.max_health
        self.shoot_cooldown = BULLET_COOLDOWN + 300
        self.special_name = "Explosive Round"
        self.special_cooldown = 10000
        
    def get_bullet_damage(self):
        return 25
        
    def _activate_special(self):
        """Fire a massive explosive round"""
        direction = 1 if self.facing_right else -1
        bullet = Bullet(
            self.rect.centerx,
            self.rect.centery,
            direction,
            50,
            explosive=True,
            speed=8
        )
        self.bullets.add(bullet)
        return "Explosive Round Fired!"


class Tech(Player):
    """Tech - Engineer with drones and hacking ability"""
    
    def __init__(self, x, y):
        super().__init__(x, y, CHARACTER_TECH)
        # Image loaded from assets/images/characters/tech_idle.png
        self.speed = PLAYER_SPEED - 1
        self.shoot_cooldown = BULLET_COOLDOWN + 100
        self.special_name = "Hack/Shield"
        self.special_cooldown = 12000
        self.drone_active = False
        self.shield_active = False
        
    def get_bullet_damage(self):
        return 12
        
    def _activate_special(self):
        """Activate energy shield that absorbs damage"""
        self.shield_active = True
        return "Shield Activated!"
        
    def take_damage(self, amount, current_time):
        if self.shield_active:
            self.shield_active = False
            return
        super().take_damage(amount, current_time)
        
    def update(self, platforms, enemies, all_sprites, current_time):
        super().update(platforms, enemies, all_sprites, current_time)
        # Shield deactivates after 5 seconds or on hit
        if self.shield_active and current_time - self.special_timer > 5000:
            self.shield_active = False
            
    def draw(self, surface, camera_x=0):
        super().draw(surface, camera_x)
        # Draw shield effect
        if self.shield_active:
            shield_surface = pygame.Surface((48, 64), pygame.SRCALPHA)
            pygame.draw.ellipse(shield_surface, (100, 150, 255, 100), shield_surface.get_rect())
            surface.blit(shield_surface, (self.rect.x - 8 - camera_x, self.rect.y - 8))


class Medic(Player):
    """Medic - Support with healing and reviving abilities"""
    
    def __init__(self, x, y):
        super().__init__(x, y, CHARACTER_MEDIC)
        # Image loaded from assets/images/characters/medic_idle.png
        self.speed = PLAYER_SPEED
        self.shoot_cooldown = BULLET_COOLDOWN + 50
        self.special_name = "Heal Pulse"
        self.special_cooldown = 15000
        
    def get_bullet_damage(self):
        return 10
        
    def _activate_special(self):
        """Heal pulse - restores health and damages nearby enemies"""
        self.health = min(self.health + 30, self.max_health)
        return "Heal Pulse! Health Restored!"
        
    def shoot(self, current_time):
        """Medic shoots healing darts (damage enemies or heal allies in multiplayer)"""
        return super().shoot(current_time)


class Stealth(Player):
    """Stealth - Invisible assassin with backstab and cloaking"""
    
    def __init__(self, x, y):
        super().__init__(x, y, CHARACTER_STEALTH)
        # Image loaded from assets/images/characters/stealth_idle.png
        self.speed = PLAYER_SPEED + 2
        self.max_health = PLAYER_MAX_HEALTH - 10
        self.health = self.max_health
        self.shoot_cooldown = BULLET_COOLDOWN - 50
        self.special_name = "Cloak"
        self.special_cooldown = 10000
        self.cloaked = False
        
    def get_bullet_damage(self):
        # Higher damage when cloaked
        return 20 if self.cloaked else 10
        
    def _activate_special(self):
        """Become invisible to enemies temporarily"""
        self.cloaked = True
        self.image.set_alpha(80)
        return "Cloak Active!"
        
    def update(self, platforms, enemies, all_sprites, current_time):
        super().update(platforms, enemies, all_sprites, current_time)
        # Decloak after 4 seconds or when shooting
        if self.cloaked and current_time - self.special_timer > 4000:
            self.decloak()
            
    def shoot(self, current_time):
        bullet = super().shoot(current_time)
        if bullet and self.cloaked:
            self.decloak()
        return bullet
        
    def decloak(self):
        self.cloaked = False
        self.image.set_alpha(255)
        
    def take_damage(self, amount, current_time):
        """Take damage forces decloak"""
        self.decloak()
        super().take_damage(amount, current_time)


def create_player(character_type, x, y):
    """Factory function to create the appropriate character"""
    characters = {
        CHARACTER_RECON: Recon,
        CHARACTER_HEAVY: Heavy,
        CHARACTER_TECH: Tech,
        CHARACTER_MEDIC: Medic,
        CHARACTER_STEALTH: Stealth
    }
    return characters.get(character_type, Recon)(x, y)
