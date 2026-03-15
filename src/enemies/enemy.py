"""
Enemy classes with different AI behaviors
"""
import pygame
import math
from src.constants import *
from src.sprite import Sprite
from src.weapons.bullet import Bullet, Explosion


class Enemy(Sprite):
    """Base enemy class"""
    
    def __init__(self, x, y, width, height, color, health, damage):
        super().__init__(x, y, width, height, color)
        self.max_health = health
        self.health = health
        self.damage = damage
        self.score_value = health * 10
        
        # AI state
        self.patrol_start = x
        self.patrol_distance = 100
        self.patrol_direction = 1
        self.detect_range = 200
        self.attack_range = 400
        self.chasing = False
        
        # Shooting
        self.can_shoot = False
        self.shoot_cooldown = 1500
        self.last_shot = 0
        self.bullets = pygame.sprite.Group()
        
        # Death
        self.dead = False
        
    def update(self, platforms, player, current_time, camera_x=0):
        """Update enemy behavior"""
        super().update()
        self.apply_gravity()
        self.check_collision_with_platforms(platforms)
        
        # Update bullets
        self.bullets.update()
        
        # Remove off-screen bullets
        for bullet in self.bullets:
            if bullet.rect.right < camera_x or bullet.rect.left > camera_x + SCREEN_WIDTH:
                bullet.kill()
                
        # Check collision with player bullets
        for bullet in player.bullets:
            if self.rect.colliderect(bullet.rect):
                if bullet.explosive:
                    # Create explosion
                    explosion = Explosion(bullet.rect.centerx, bullet.rect.centery)
                    # Deal damage in area
                    self.take_damage(bullet.damage)
                else:
                    self.take_damage(bullet.damage)
                bullet.kill()
                
    def take_damage(self, amount):
        """Take damage"""
        self.health -= amount
        if self.health <= 0:
            self.dead = True
            self.kill()
            return self.score_value
        return 0
        
    def shoot_at_player(self, player, current_time):
        """Shoot at player if in range"""
        if not self.can_shoot:
            return
            
        if current_time - self.last_shot > self.shoot_cooldown:
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance < self.attack_range:
                self.last_shot = current_time
                direction = 1 if dx > 0 else -1
                bullet = Bullet(
                    self.rect.centerx,
                    self.rect.centery - 10,
                    direction,
                    self.damage,
                    speed=8
                )
                self.bullets.add(bullet)
                
    def draw(self, surface, camera_x=0):
        """Draw enemy and bullets"""
        for bullet in self.bullets:
            bullet.draw(surface, camera_x)
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y))
        
        # Draw health bar
        bar_width = self.rect.width
        bar_height = 4
        health_pct = self.health / self.max_health
        pygame.draw.rect(surface, RED, (self.rect.x - camera_x, self.rect.y - 8, bar_width, bar_height))
        pygame.draw.rect(surface, GREEN, (self.rect.x - camera_x, self.rect.y - 8, bar_width * health_pct, bar_height))


class PatrolEnemy(Enemy):
    """Basic enemy that patrols back and forth"""
    
    def __init__(self, x, y, patrol_distance=100):
        super().__init__(x, y, 32, 32, ORANGE, 30, 10)
        self.patrol_distance = patrol_distance
        self.patrol_start = x
        self.speed = 2
        self.score_value = 100
        
    def update(self, platforms, player, current_time, camera_x=0):
        super().update(platforms, player, current_time, camera_x)
        
        if self.dead:
            return
            
        # Simple patrol behavior
        self.vel_x = self.speed * self.patrol_direction
        
        # Turn around at patrol boundaries
        if self.rect.x > self.patrol_start + self.patrol_distance:
            self.patrol_direction = -1
            self.facing_right = False
        elif self.rect.x < self.patrol_start:
            self.patrol_direction = 1
            self.facing_right = True
            
        # Chase if player is close
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance < self.detect_range:
            if abs(dx) > 5:
                self.vel_x = self.speed * 2 * (1 if dx > 0 else -1)
                self.facing_right = dx > 0


class TurretEnemy(Enemy):
    """Stationary turret that shoots at player"""
    
    def __init__(self, x, y):
        super().__init__(x, y, 40, 40, RED, 50, 15)
        self.can_shoot = True
        self.score_value = 200
        
    def update(self, platforms, player, current_time, camera_x=0):
        super().update(platforms, player, current_time, camera_x)
        
        if self.dead:
            return
            
        # Always face player
        dx = player.rect.centerx - self.rect.centerx
        self.facing_right = dx > 0
        
        # Shoot at player
        self.shoot_at_player(player, current_time)


class FlyingEnemy(Enemy):
    """Flying enemy that doesn't obey gravity"""
    
    def __init__(self, x, y):
        super().__init__(x, y, 36, 24, CYAN, 25, 12)
        self.score_value = 150
        self.speed = 3
        self.fly_height = y
        self.can_shoot = True
        self.shoot_cooldown = 2000
        
    def apply_gravity(self):
        """Flying enemies don't fall"""
        pass
        
    def check_collision_with_platforms(self, platforms):
        """Flying enemies pass through platforms"""
        pass
        
    def update(self, platforms, player, current_time, camera_x=0):
        super().update(platforms, player, current_time, camera_x)
        
        if self.dead:
            return
            
        # Hover at fly height with slight bobbing
        self.rect.y = self.fly_height + int(20 * math.sin(current_time / 500))
        
        # Move toward player
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 50:
            if abs(dx) > 5:
                self.vel_x = self.speed * (1 if dx > 0 else -1)
                self.facing_right = dx > 0
        else:
            self.vel_x = 0
            
        # Shoot at player
        self.shoot_at_player(player, current_time)


class BossEnemy(Enemy):
    """Powerful boss enemy"""
    
    def __init__(self, x, y):
        super().__init__(x, y, 80, 100, MAGENTA, 500, 25)
        self.score_value = 5000
        self.speed = 2
        self.can_shoot = True
        self.shoot_cooldown = 800
        self.phase = 1
        self.max_phases = 3
        
    def update(self, platforms, player, current_time, camera_x=0):
        super().update(platforms, player, current_time, camera_x)
        
        if self.dead:
            return
            
        # Determine phase based on health
        health_pct = self.health / self.max_health
        if health_pct < 0.3:
            self.phase = 3
        elif health_pct < 0.6:
            self.phase = 2
            
        # Boss behavior
        dx = player.rect.centerx - self.rect.centerx
        
        # Phase-based behavior
        if self.phase == 1:
            # Phase 1: Move slowly and shoot
            if abs(dx) > 100:
                self.vel_x = self.speed * (1 if dx > 0 else -1)
            else:
                self.vel_x = 0
        elif self.phase == 2:
            # Phase 2: Faster movement, rapid fire
            self.shoot_cooldown = 500
            if abs(dx) > 50:
                self.vel_x = self.speed * 2 * (1 if dx > 0 else -1)
        else:
            # Phase 3: Very aggressive, multi-shot
            self.shoot_cooldown = 300
            self.vel_x = self.speed * 1.5 * (1 if dx > 0 else -1)
            
        self.facing_right = dx > 0
        
        # Shoot - boss fires multiple bullets
        if current_time - self.last_shot > self.shoot_cooldown:
            self.last_shot = current_time
            direction = 1 if self.facing_right else -1
            
            # Always shoot straight
            bullet1 = Bullet(self.rect.centerx, self.rect.centery - 20, direction, self.damage, speed=10)
            self.bullets.add(bullet1)
            
            if self.phase >= 2:
                # Phase 2+: Shoot angled shots
                bullet2 = Bullet(self.rect.centerx, self.rect.centery - 20, direction, self.damage, speed=9)
                bullet2.vel_y = -3
                self.bullets.add(bullet2)
                
            if self.phase >= 3:
                # Phase 3+: Triple shot
                bullet3 = Bullet(self.rect.centerx, self.rect.centery - 20, direction, self.damage, speed=9)
                bullet3.vel_y = 3
                self.bullets.add(bullet3)


def create_enemy(enemy_type, x, y, **kwargs):
    """Factory function to create enemies"""
    enemies = {
        ENEMY_PATROL: PatrolEnemy,
        ENEMY_TURRET: TurretEnemy,
        ENEMY_FLYING: FlyingEnemy,
        ENEMY_BOSS: BossEnemy
    }
    
    enemy_class = enemies.get(enemy_type, PatrolEnemy)
    if enemy_type == ENEMY_PATROL:
        return enemy_class(x, y, kwargs.get('patrol_distance', 100))
    return enemy_class(x, y)
