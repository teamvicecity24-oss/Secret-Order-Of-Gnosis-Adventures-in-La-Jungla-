"""
UI components for game menus and HUD
"""
import pygame
from src.constants import *


class Button:
    """Clickable button"""
    
    def __init__(self, x, y, width, height, text, color=GRAY, hover_color=WHITE, text_color=BLACK):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.hovered = False
        self.font = pygame.font.Font(None, 36)
        
    def draw(self, surface):
        """Draw button"""
        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 2)
        
        # Draw text
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def update(self, mouse_pos):
        """Update hover state"""
        self.hovered = self.rect.collidepoint(mouse_pos)
        
    def is_clicked(self, event):
        """Check if button was clicked"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False


class GlowingButton(Button):
    """Button with yellow glow effect and black outline"""
    
    def __init__(self, x, y, width, height, text, action=None):
        super().__init__(x, y, width, height, text, action=action)
        self.glow_radius = 0
        self.glow_direction = 1
        self.glow_timer = 0
        
        # Yellow button colors
        self.color = (255, 215, 0)  # Gold/Yellow
        self.hover_color = (255, 255, 100)  # Bright yellow
        self.text_color = BLACK
        self.outline_color = BLACK
        self.glow_color = (255, 200, 50)
        
    def update(self, mouse_pos):
        """Update glow animation and hover state"""
        super().update(mouse_pos)
        
        # Animate glow
        self.glow_timer += 1
        self.glow_radius = 8 + int(4 * pygame.math.Vector2(1, 0).rotate(self.glow_timer * 3).y)
        
    def draw(self, surface):
        """Draw glowing yellow button with black outline"""
        # Get current color
        color = self.hover_color if self.hovered else self.color
        
        # Draw glow effect (multiple layers for intensity)
        if self.hovered:
            for i in range(3, 0, -1):
                glow_surface = pygame.Surface((self.rect.width + self.glow_radius * 2, 
                                              self.rect.height + self.glow_radius * 2), 
                                             pygame.SRCALPHA)
                pygame.draw.rect(glow_surface, (*self.glow_color, 60 - i * 15), 
                                (self.glow_radius - i * 2, self.glow_radius - i * 2,
                                 self.rect.width + i * 4, self.rect.height + i * 4),
                                border_radius=8)
                surface.blit(glow_surface, 
                           (self.rect.x - self.glow_radius, self.rect.y - self.glow_radius))
        
        # Draw button background
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        
        # Draw black outline
        pygame.draw.rect(surface, self.outline_color, self.rect, 3, border_radius=5)
        
        # Inner highlight
        pygame.draw.rect(surface, (255, 255, 200), 
                        (self.rect.x + 2, self.rect.y + 2, 
                         self.rect.width - 4, self.rect.height // 2 - 2), 
                        border_radius=3)
        
        # Draw text
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)


class Menu:
    """Base menu class"""
    
    def __init__(self, title):
        self.title = title
        self.buttons = []
        self.font_title = pygame.font.Font(None, 72)
        self.font_text = pygame.font.Font(None, 36)
        self.active = False
        
    def add_button(self, x, y, width, height, text, action=None):
        """Add a button to the menu"""
        button = Button(x, y, width, height, text)
        button.action = action
        self.buttons.append(button)
        return button
        
    def update(self, mouse_pos, events):
        """Update menu state"""
        for button in self.buttons:
            button.update(mouse_pos)
            for event in events:
                if button.is_clicked(event) and button.action:
                    return button.action()
        return None
        
    def draw(self, surface):
        """Draw menu"""
        # Title
        title_surf = self.font_title.render(self.title, True, WHITE)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 100))
        surface.blit(title_surf, title_rect)
        
        # Buttons
        for button in self.buttons:
            button.draw(surface)


class MainMenu(Menu):
    """Main game menu"""
    
    def __init__(self):
        super().__init__("Secret Order of Gnosis")
        self.subtitle = "Adventures in La Jungla"
        
        # Load full-screen background image (the seal)
        try:
            self.bg_image = pygame.image.load('assets/images/ui/logo.png').convert()
            # Scale to fill screen
            self.bg_image = pygame.transform.scale(self.bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            # Fallback to black
            self.bg_image = None
        
        # Create glowing yellow buttons with black outline
        center_x = SCREEN_WIDTH // 2 - 100
        button_y_start = 320
        button_spacing = 70
        
        self.buttons = []  # Clear default buttons
        self._create_glowing_button(center_x, button_y_start, 200, 50, "Play", lambda: "play")
        self._create_glowing_button(center_x, button_y_start + button_spacing, 200, 50, "Character Select", lambda: "character_select")
        self._create_glowing_button(center_x, button_y_start + button_spacing * 2, 200, 50, "High Scores", lambda: "high_scores")
        self._create_glowing_button(center_x, button_y_start + button_spacing * 3, 200, 50, "Help", lambda: "help")
        self._create_glowing_button(center_x, button_y_start + button_spacing * 4, 200, 50, "Quit", lambda: "quit")
        
    def _create_glowing_button(self, x, y, width, height, text, action):
        """Create a glowing yellow button with black outline"""
        # Custom button with glow effect
        button = GlowingButton(x, y, width, height, text, action)
        self.buttons.append(button)
        return button
        
    def draw(self, surface):
        """Draw main menu with seal background and glowing buttons"""
        # Draw full-screen background (the seal)
        if self.bg_image:
            surface.blit(self.bg_image, (0, 0))
        else:
            surface.fill(BLACK)
        
        # Title at top with glow
        title_surf = self.font_title.render(self.title, True, (255, 215, 0))  # Gold
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 60))
        
        # Title glow effect
        for offset in range(3, 0, -1):
            glow_surf = self.font_title.render(self.title, True, (255, 180, 0))
            surface.blit(glow_surf, (title_rect.x + offset, title_rect.y + offset))
        surface.blit(title_surf, title_rect)
        
        # Subtitle
        sub_surf = self.font_text.render(self.subtitle, True, (255, 255, 150))
        sub_rect = sub_surf.get_rect(center=(SCREEN_WIDTH // 2, 105))
        surface.blit(sub_surf, sub_rect)
        
        # Glowing buttons
        for button in self.buttons:
            button.draw(surface)


class CharacterSelectMenu(Menu):
    """Character selection screen - Jungle/Adventure Theme"""
    
    def __init__(self):
        super().__init__("Choose Your Operative")
        
        # Jungle/Adventure color scheme
        self.bg_color = (20, 40, 20)  # Dark jungle green
        self.title_color = (255, 215, 100)  # Golden yellow
        self.text_color = (220, 220, 200)  # Light cream
        self.highlight_color = (255, 180, 60)  # Orange-gold
        self.box_border = (100, 80, 50)  # Brown
        
        self.characters = [
            ("Recon", (0, 200, 255), "Speedster with rapid fire", "Speed Boost"),
            ("Heavy", (200, 50, 50), "Tank with explosive rounds", "Explosive Round"),
            ("Tech", (100, 150, 255), "Engineer with energy shield", "Shield"),
            ("Medic", (50, 200, 100), "Support with healing pulse", "Heal Pulse"),
            ("Stealth", (150, 50, 200), "Invisible assassin", "Cloak"),
        ]
        
        self.selected = 0
        self.font_small = pygame.font.Font(None, 28)
        
        # Back button
        self.add_button(50, SCREEN_HEIGHT - 100, 150, 50, "Back", lambda: "back")
        self.add_button(SCREEN_WIDTH - 200, SCREEN_HEIGHT - 100, 150, 50, "Select", lambda: "confirm")
        
    def update(self, mouse_pos, events):
        """Update selection"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.selected = (self.selected - 1) % len(self.characters)
                elif event.key == pygame.K_RIGHT:
                    self.selected = (self.selected + 1) % len(self.characters)
                elif event.key == pygame.K_RETURN:
                    return self.characters[self.selected][0].lower()
                    
        return super().update(mouse_pos, events)
        
    def draw(self, surface):
        """Draw character selection with jungle theme"""
        surface.fill(self.bg_color)
        
        # Draw decorative border
        pygame.draw.rect(surface, self.box_border, (10, 10, SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20), 3)
        
        # Title with shadow effect
        title_surf = self.font_title.render(self.title, True, self.title_color)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 60))
        # Shadow
        shadow_surf = self.font_title.render(self.title, True, (50, 40, 20))
        surface.blit(shadow_surf, (title_rect.x + 3, title_rect.y + 3))
        surface.blit(title_surf, title_rect)
        
        # Subtitle
        subtitle = "Secret Order of Gnosis"
        sub_surf = self.font_text.render(subtitle, True, (180, 160, 100))
        sub_rect = sub_surf.get_rect(center=(SCREEN_WIDTH // 2, 110))
        surface.blit(sub_surf, sub_rect)
        
        # Draw characters
        box_width = 180
        box_height = 200
        spacing = 40
        start_x = (SCREEN_WIDTH - (len(self.characters) * box_width + (len(self.characters) - 1) * spacing)) // 2
        
        for i, (name, color, desc, special) in enumerate(self.characters):
            x = start_x + i * (box_width + spacing)
            y = 160
            
            # Selection box with border
            box_rect = pygame.Rect(x, y, box_width, box_height)
            if i == self.selected:
                # Glow effect for selected
                pygame.draw.rect(surface, self.highlight_color, box_rect.inflate(12, 12))
                pygame.draw.rect(surface, (255, 255, 255), box_rect.inflate(8, 8), 2)
            pygame.draw.rect(surface, self.box_border, box_rect.inflate(4, 4))
            pygame.draw.rect(surface, color, box_rect)
            
            # Character icon placeholder (could load actual images here)
            icon_rect = pygame.Rect(x + 70, y + 15, 40, 40)
            pygame.draw.rect(surface, (0, 0, 0, 100), icon_rect)
            pygame.draw.rect(surface, WHITE, icon_rect, 2)
            
            # Character name
            name_surf = self.font_text.render(name, True, WHITE)
            name_rect = name_surf.get_rect(center=(x + box_width // 2, y + 70))
            surface.blit(name_surf, name_rect)
            
            # Description
            words = desc.split()
            lines = []
            line = []
            for word in words:
                line.append(word)
                if len(' '.join(line)) > 20:
                    lines.append(' '.join(line[:-1]))
                    line = [line[-1]]
            if line:
                lines.append(' '.join(line))
                
            for j, line in enumerate(lines):
                desc_surf = self.font_small.render(line, True, self.text_color)
                desc_rect = desc_surf.get_rect(center=(x + box_width // 2, y + 115 + j * 22))
                surface.blit(desc_surf, desc_rect)
            
            # Special ability label
            special_label = self.font_small.render("Special Ability:", True, (180, 160, 100))
            surface.blit(special_label, (x + box_width // 2 - 50, y + 155))
            
            special_surf = self.font_small.render(special, True, self.highlight_color)
            special_rect = special_surf.get_rect(center=(x + box_width // 2, y + 180))
            surface.blit(special_surf, special_rect)
        
        # Buttons
        for button in self.buttons:
            button.draw(surface)
            
    def get_selected_character(self):
        """Get currently selected character type"""
        return self.characters[self.selected][0].lower()


class PauseMenu(Menu):
    """Pause menu"""
    
    def __init__(self):
        super().__init__("PAUSED")
        
        center_x = SCREEN_WIDTH // 2 - 100
        self.add_button(center_x, 280, 200, 50, "Resume", lambda: "resume")
        self.add_button(center_x, 350, 200, 50, "Restart Level", lambda: "restart")
        self.add_button(center_x, 420, 200, 50, "Quit to Menu", lambda: "quit")
        
    def draw(self, surface):
        """Draw pause overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        surface.blit(overlay, (0, 0))
        
        super().draw(surface)


class GameOverMenu(Menu):
    """Game over screen"""
    
    def __init__(self, score=0, won=False):
        title = "VICTORY!" if won else "GAME OVER"
        super().__init__(title)
        self.score = score
        self.won = won
        
        center_x = SCREEN_WIDTH // 2 - 100
        self.add_button(center_x, 380, 200, 50, "Play Again", lambda: "restart")
        self.add_button(center_x, 450, 200, 50, "Main Menu", lambda: "menu")
        
    def draw(self, surface):
        """Draw game over screen"""
        surface.fill(BLACK)
        
        # Title
        color = GREEN if self.won else RED
        title_surf = self.font_title.render(self.title, True, color)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 200))
        surface.blit(title_surf, title_rect)
        
        # Score
        score_surf = self.font_text.render(f"Final Score: {self.score}", True, WHITE)
        score_rect = score_surf.get_rect(center=(SCREEN_WIDTH // 2, 300))
        surface.blit(score_surf, score_rect)
        
        # Buttons
        for button in self.buttons:
            button.draw(surface)


class HUD:
    """In-game HUD"""
    
    def __init__(self):
        self.font = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
    def draw(self, surface, player, score_manager, level_number):
        """Draw HUD elements"""
        # Health bar
        health_width = 200
        health_height = 20
        health_x = 20
        health_y = 20
        
        health_pct = player.health / player.max_health
        pygame.draw.rect(surface, DARK_GRAY, (health_x, health_y, health_width, health_height))
        pygame.draw.rect(surface, RED, (health_x, health_y, health_width * health_pct, health_height))
        pygame.draw.rect(surface, WHITE, (health_x, health_y, health_width, health_height), 2)
        
        # Health text
        health_text = self.font.render(f"{int(player.health)}/{player.max_health}", True, WHITE)
        surface.blit(health_text, (health_x + health_width + 10, health_y))
        
        # Character name
        char_text = self.font.render(player.character_type.upper(), True, WHITE)
        surface.blit(char_text, (health_x, health_y + 30))
        
        # Special ability cooldown
        if player.special_timer > 0:
            cooldown_pct = 1 - (pygame.time.get_ticks() - player.special_timer) / player.special_cooldown
            bar_width = 150
            pygame.draw.rect(surface, DARK_GRAY, (health_x, health_y + 60, bar_width, 10))
            pygame.draw.rect(surface, YELLOW, (health_x, health_y + 60, bar_width * cooldown_pct, 10))
            special_text = self.font_small.render(f"{player.special_name}", True, YELLOW)
        else:
            special_text = self.font_small.render(f"{player.special_name} [SPACE] Ready!", True, GREEN)
        surface.blit(special_text, (health_x, health_y + 75))
        
        # Score
        score_text = self.font.render(f"Score: {score_manager.get_current_score()}", True, WHITE)
        surface.blit(score_text, (SCREEN_WIDTH - 200, 20))
        
        # Level
        level_text = self.font.render(f"Level {level_number}", True, WHITE)
        surface.blit(level_text, (SCREEN_WIDTH - 200, 50))
        
        # Controls hint
        hint_text = self.font_small.render("WASD/Arrows: Move | SPACE: Special | E: Interact", True, GRAY)
        surface.blit(hint_text, (20, SCREEN_HEIGHT - 30))


class HighScoreMenu(Menu):
    """High scores display"""
    
    def __init__(self, score_manager):
        super().__init__("High Scores")
        self.score_manager = score_manager
        self.add_button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50, "Back", lambda: "back")
        
    def draw(self, surface):
        """Draw high scores"""
        surface.fill(BLACK)
        
        # Title
        title_surf = self.font_title.render(self.title, True, YELLOW)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 50))
        surface.blit(title_surf, title_rect)
        
        # Headers
        headers = ["Rank", "Name", "Score", "Enemies", "Coins", "Time"]
        x_positions = [80, 180, 350, 500, 620, 720]
        for i, header in enumerate(headers):
            header_surf = self.font_text.render(header, True, CYAN)
            surface.blit(header_surf, (x_positions[i], 120))
        
        # Scores
        scores = self.score_manager.get_high_scores(10)
        for i, score in enumerate(scores):
            y = 160 + i * 40
            color = WHITE if i > 0 else YELLOW  # Highlight #1
            
            rank_surf = self.font_text.render(str(i + 1), True, color)
            surface.blit(rank_surf, (x_positions[0], y))
            
            name_surf = self.font_text.render(score['name'], True, color)
            surface.blit(name_surf, (x_positions[1], y))
            
            score_surf = self.font_text.render(str(score['score']), True, color)
            surface.blit(score_surf, (x_positions[2], y))
            
            enemy_surf = self.font_text.render(str(score['enemies']), True, color)
            surface.blit(enemy_surf, (x_positions[3], y))
            
            coin_surf = self.font_text.render(str(score['coins']), True, color)
            surface.blit(coin_surf, (x_positions[4], y))
            
            time_surf = self.font_text.render(f"{score['time']}s", True, color)
            surface.blit(time_surf, (x_positions[5], y))
        
        # Button
        for button in self.buttons:
            button.draw(surface)
