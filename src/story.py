"""
Story and Lore System for Secret Order of Gnosis
Includes Keepers, PEEL dialogue, and story progression
"""
import pygame
from src.constants import *


class StoryManager:
    """Manages game story, lore, and keeper progression"""
    
    def __init__(self):
        # Story progression
        self.current_chapter = 0
        self.unlocked_keepers = []
        self.peel_dialogue_queue = []
        
        # Keepers data
        self.keepers = {
            'flame': {
                'name': 'Keeper of Flame',
                'level': 1,
                'power': 'Fire Rounds',
                'description': 'Grants burning bullets that damage over time',
                'color': (255, 100, 0),
                'rescued': False
            },
            'echo': {
                'name': 'Keeper of Echo',
                'level': 2,
                'power': 'Double Jump',
                'description': 'Grants the ability to jump twice in mid-air',
                'color': (100, 200, 255),
                'rescued': False
            },
            'ether': {
                'name': 'Keeper of Ether',
                'level': 3,
                'power': 'Shard Magnet',
                'description': 'Automatically attracts nearby coins and collectibles',
                'color': (200, 100, 255),
                'rescued': False
            }
        }
        
        # PEEL dialogue lines
        self.peel_hints = {
            'intro': [
                "VICE... wake up...",
                "The Keepers of Gnosis await.",
                "I am PEEL, fragment of UGA.",
                "Let me guide you through the jungle."
            ],
            'movement': [
                "Use WASD or Arrows to move.",
                "Jump with UP or W.",
                "Don't fall into the void!"
            ],
            'combat': [
                "Press CTRL or F to shoot.",
                "Q activates your special ability.",
                "Defeat enemies to gain score."
            ],
            'keeper_flame': [
                "A Keeper is near...",
                "The Keeper of Flame hides ahead.",
                "Rescue them to gain Fire Rounds!"
            ],
            'keeper_echo': [
                "I sense the Keeper of Echo...",
                "They will grant you the double jump.",
                "Search the high platforms."
            ],
            'keeper_ether': [
                "The final Keeper awaits...",
                "Keeper of Ether holds the magnet power.",
                "Collect all to reach UGA's prison."
            ],
            'secrets': [
                "Something glows in the shadows...",
                "Check behind the waterfalls!",
                "Hidden paths lead to treasure."
            ]
        }
        
    def rescue_keeper(self, keeper_id):
        """Mark a keeper as rescued and grant their power"""
        if keeper_id in self.keepers and not self.keepers[keeper_id]['rescued']:
            self.keepers[keeper_id]['rescued'] = True
            self.unlocked_keepers.append(keeper_id)
            return self.keepers[keeper_id]
        return None
        
    def get_keeper_for_level(self, level_number):
        """Get the keeper associated with a level"""
        for keeper_id, data in self.keepers.items():
            if data['level'] == level_number:
                return keeper_id, data
        return None, None
        
    def has_power(self, power_name):
        """Check if player has unlocked a specific power"""
        for keeper_id in self.unlocked_keepers:
            if self.keepers[keeper_id]['power'] == power_name:
                return True
        return False
        
    def get_peel_hint(self, context='intro'):
        """Get a hint from PEEL based on context"""
        import random
        if context in self.peel_hints:
            return random.choice(self.peel_hints[context])
        return "PEEL says: Keep going, VICE!"


class Keeper(pygame.sprite.Sprite):
    """Keeper NPC that grants powers when rescued"""
    
    def __init__(self, x, y, keeper_id, story_manager):
        super().__init__()
        self.keeper_id = keeper_id
        self.story_manager = story_manager
        self.data = story_manager.keepers[keeper_id]
        
        # Visual
        self.image = pygame.Surface((48, 64), pygame.SRCALPHA)
        self.color = self.data['color']
        self._draw_keeper()
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Animation
        self.bob_offset = 0
        self.glow_radius = 0
        
        # Interaction
        self.interact_range = 60
        self.rescued = False
        
    def _draw_keeper(self):
        """Draw keeper appearance"""
        # Glowing orb body
        pygame.draw.ellipse(self.image, (*self.color, 200), 
                          (8, 16, 32, 48))
        # Inner core
        pygame.draw.ellipse(self.image, (*self.color, 255), 
                          (12, 24, 24, 32))
        # Crown/halo
        pygame.draw.polygon(self.image, (255, 215, 0), 
                          [(24, 8), (16, 20), (32, 20)])
        
    def update(self):
        """Animate keeper floating"""
        self.bob_offset += 0.1
        self.glow_radius = 20 + int(5 * pygame.math.Vector2(1, 0).rotate(self.bob_offset * 30).y)
        
    def can_interact(self, player):
        """Check if player is close enough to rescue"""
        distance = pygame.math.Vector2(
            player.rect.centerx - self.rect.centerx,
            player.rect.centery - self.rect.centery
        ).length()
        return distance < self.interact_range
        
    def rescue(self):
        """Rescue this keeper"""
        if not self.rescued:
            self.rescued = True
            return self.story_manager.rescue_keeper(self.keeper_id)
        return None
        
    def draw(self, surface, camera_x=0):
        """Draw keeper with glow effect"""
        if self.rescued:
            return
            
        # Draw glow
        glow_surface = pygame.Surface((96, 96), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (*self.color, 50), 
                          (48, 48), self.glow_radius)
        surface.blit(glow_surface, 
                    (self.rect.centerx - 48 - camera_x, 
                     self.rect.centery - 48))
        
        # Draw keeper with bob animation
        y_offset = int(5 * pygame.math.Vector2(1, 0).rotate(self.bob_offset * 50).y)
        surface.blit(self.image, 
                    (self.rect.x - camera_x, 
                     self.rect.y + y_offset))
        
        # Draw interaction prompt
        pygame.draw.circle(surface, WHITE, 
                          (self.rect.centerx - camera_x, 
                           self.rect.top - 20 + y_offset), 5)


class PEELCompanion:
    """PEEL the banana guide - provides hints and comic relief"""
    
    def __init__(self, story_manager):
        self.story_manager = story_manager
        self.current_dialogue = ""
        self.dialogue_timer = 0
        self.visible = True
        self.bob_offset = 0
        
        # PEEL visual (banana shape)
        self.image = pygame.Surface((32, 40), pygame.SRCALPHA)
        self._draw_peel()
        
    def _draw_peel(self):
        """Draw PEEL's banana appearance"""
        # Banana body (yellow curve)
        color = (255, 220, 50)  # Banana yellow
        pygame.draw.ellipse(self.image, color, (4, 8, 24, 28))
        # Stem
        pygame.draw.rect(self.image, (139, 90, 43), (12, 2, 8, 8))
        # Tips
        pygame.draw.circle(self.image, (100, 100, 100), (16, 34), 3)
        # Glow effect for "fragment of UGA"
        pygame.draw.ellipse(self.image, (255, 255, 200, 100), 
                          (2, 4, 28, 32), 2)
        
    def show_hint(self, context='intro'):
        """Show a hint from PEEL"""
        self.current_dialogue = self.story_manager.get_peel_hint(context)
        self.dialogue_timer = 300  # Show for 5 seconds at 60fps
        
    def update(self):
        """Update PEEL animation"""
        self.bob_offset += 0.15
        if self.dialogue_timer > 0:
            self.dialogue_timer -= 1
            
    def draw(self, surface, player_x, player_y, camera_x=0):
        """Draw PEEL floating near player with dialogue"""
        if not self.visible:
            return
            
        # Position near player
        peel_x = player_x - camera_x - 40
        peel_y = player_y + int(8 * pygame.math.Vector2(1, 0).rotate(self.bob_offset * 50).y)
        
        # Draw PEEL
        surface.blit(self.image, (peel_x, peel_y))
        
        # Draw glow (fragment of UGA)
        glow_surface = pygame.Surface((48, 48), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (255, 255, 100, 80), 
                          (24, 24), 16 + int(4 * pygame.math.Vector2(1, 0).rotate(self.bob_offset * 60).y))
        surface.blit(glow_surface, (peel_x - 8, peel_y - 4))
        
        # Draw dialogue box if active
        if self.dialogue_timer > 0:
            self._draw_dialogue(surface, peel_x, peel_y)
            
    def _draw_dialogue(self, surface, peel_x, peel_y):
        """Draw PEEL's dialogue box"""
        # Box dimensions
        text = self.current_dialogue
        font = pygame.font.Font(None, 24)
        text_surf = font.render(text, True, (255, 255, 200))
        
        box_width = text_surf.get_width() + 20
        box_height = 30
        box_x = peel_x + 40
        box_y = peel_y - 10
        
        # Keep on screen
        if box_x + box_width > SCREEN_WIDTH:
            box_x = peel_x - box_width - 10
            
        # Draw box
        pygame.draw.rect(surface, (30, 40, 30, 200), 
                        (box_x, box_y, box_width, box_height))
        pygame.draw.rect(surface, (100, 150, 100), 
                        (box_x, box_y, box_width, box_height), 2)
        
        # Draw text
        surface.blit(text_surf, (box_x + 10, box_y + 5))
        
        # Draw PEEL indicator
        pygame.draw.line(surface, (100, 150, 100), 
                        (peel_x + 32, peel_y + 20),
                        (box_x, box_y + 15), 2)


class LoreScreen:
    """Screen for displaying story lore and keeper info"""
    
    def __init__(self, story_manager):
        self.story_manager = story_manager
        self.font_title = pygame.font.Font(None, 48)
        self.font_text = pygame.font.Font(None, 28)
        
    def draw(self, surface):
        """Draw lore screen showing rescued keepers"""
        surface.fill((20, 30, 20))
        
        # Title
        title = self.font_title.render("The Secret Order of Gnosis", True, (255, 215, 100))
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 30))
        
        # Story text
        story_lines = [
            "Uga's chosen guardians of knowledge.",
            "Hidden throughout the realm of La Jungla.",
            "Rescue the Keepers to awaken your powers.",
            "",
            "Rescued Keepers:"
        ]
        
        y = 100
        for line in story_lines:
            text = self.font_text.render(line, True, (200, 200, 180))
            surface.blit(text, (100, y))
            y += 35
            
        # Show rescued keepers
        y += 20
        for keeper_id in self.story_manager.unlocked_keepers:
            data = self.story_manager.keepers[keeper_id]
            
            # Keeper name
            name = self.font_title.render(data['name'], True, data['color'])
            surface.blit(name, (120, y))
            y += 40
            
            # Power granted
            power = self.font_text.render(f"Power: {data['power']}", True, (255, 255, 200))
            surface.blit(power, (140, y))
            y += 25
            
            # Description
            desc = self.font_text.render(data['description'], True, (180, 180, 160))
            surface.blit(desc, (140, y))
            y += 50
            
        # Show PEEL info
        y += 30
        peel_title = self.font_title.render("PEEL - Your Guide", True, (255, 220, 50))
        surface.blit(peel_title, (100, y))
        y += 40
        
        peel_desc = [
            "A fragment of UGA, guiding you through the jungle.",
            "Listen to PEEL's hints to find hidden paths and Keepers."
        ]
        for line in peel_desc:
            text = self.font_text.render(line, True, (200, 200, 180))
            surface.blit(text, (120, y))
            y += 30
            
        # Instructions
        hint = self.font_text.render("Press ESC or click to return", True, (150, 150, 150))
        surface.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 50))
