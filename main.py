"""
Secret Order of Gnosis: Adventures in La Jungla
Main Game File

A 2D platformer shooter with 5 unique characters, puzzles, and multiple levels.
"""
import pygame
import sys

from src.constants import *
from src.characters.player import create_player
from src.levels.level import Level, LEVEL_0_DATA, LEVEL_1_DATA, LEVEL_2_DATA, LEVEL_3_DATA
from src.scoring import ScoreManager
from src.ui.menu import (
    MainMenu, CharacterSelectMenu, PauseMenu, 
    GameOverMenu, HUD, HighScoreMenu
)
from src.story import StoryManager, PEELCompanion, Keeper, LoreScreen


class Game:
    """Main game class"""
    
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Game state
        self.state = STATE_MENU
        self.current_level = 0
        self.max_levels = 4
        self.selected_character = CHARACTER_RECON
        
        # Game objects
        self.player = None
        self.level = None
        self.score_manager = ScoreManager()
        
        # Story system - Secret Order of Gnosis
        self.story_manager = StoryManager()
        self.peel = PEELCompanion(self.story_manager)
        self.lore_screen = LoreScreen(self.story_manager)
        self.current_keeper = None
        
        # Menus
        self.main_menu = MainMenu()
        self.character_select = CharacterSelectMenu()
        self.pause_menu = PauseMenu()
        self.hud = HUD()
        self.high_score_menu = None
        self.game_over_menu = None
        
        # Input
        self.keys = None
        
        # Show intro after short delay
        self.game_start_timer = 0
        
    def run(self):
        """Main game loop"""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # Delta time in seconds
            
            # Handle events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.state == STATE_PLAYING:
                            self.state = STATE_PAUSE
                        elif self.state == STATE_PAUSE:
                            self.state = STATE_PLAYING
                            
            # Update and render based on state
            if self.state == STATE_MENU:
                self.update_menu(events)
            elif self.state == STATE_CHARACTER_SELECT:
                self.update_character_select(events)
            elif self.state == STATE_PLAYING:
                self.update_playing(dt, events)
            elif self.state == STATE_PAUSE:
                self.update_pause(events)
            elif self.state == STATE_GAME_OVER:
                self.update_game_over(events)
            elif self.state == STATE_LEVEL_COMPLETE:
                self.update_level_complete(events)
            elif self.state == "high_scores":
                self.update_high_scores(events)
                
            pygame.display.flip()
            
        pygame.quit()
        sys.exit()
        
    def update_menu(self, events):
        """Update main menu"""
        mouse_pos = pygame.mouse.get_pos()
        result = self.main_menu.update(mouse_pos, events)
        
        if result == "play":
            self.start_game()
        elif result == "character_select":
            self.state = STATE_CHARACTER_SELECT
        elif result == "high_scores":
            self.high_score_menu = HighScoreMenu(self.score_manager)
            self.state = "high_scores"
        elif result == "quit":
            self.running = False
            
        self.main_menu.draw(self.screen)
        
    def update_character_select(self, events):
        """Update character selection"""
        mouse_pos = pygame.mouse.get_pos()
        result = self.character_select.update(mouse_pos, events)
        
        if result == "back":
            self.state = STATE_MENU
        elif result == "confirm":
            self.selected_character = self.character_select.get_selected_character()
            self.start_game()
        elif result in [CHARACTER_RECON, CHARACTER_HEAVY, CHARACTER_TECH, CHARACTER_MEDIC, CHARACTER_STEALTH]:
            self.selected_character = result
            self.start_game()
            
        self.character_select.draw(self.screen)
        
    def update_playing(self, dt, events):
        """Update gameplay"""
        current_time = pygame.time.get_ticks()
        self.keys = pygame.key.get_pressed()
        
        # Player movement
        if self.keys[pygame.K_LEFT] or self.keys[pygame.K_a]:
            self.player.move_left(self.player.speed)
        elif self.keys[pygame.K_RIGHT] or self.keys[pygame.K_d]:
            self.player.move_right(self.player.speed)
        else:
            self.player.stop_horizontal()
            
        if self.keys[pygame.K_UP] or self.keys[pygame.K_w]:
            # Jump only on key press events
            for event in events:
                if event.type == pygame.KEYDOWN and event.key in [pygame.K_UP, pygame.K_w]:
                    self.player.jump()
                    
        # Shooting
        if self.keys[pygame.K_LCTRL] or self.keys[pygame.K_RCTRL] or self.keys[pygame.K_f]:
            bullet = self.player.shoot(current_time)
            if bullet:
                all_sprites = pygame.sprite.Group()
                all_sprites.add(bullet)
                
        # Special ability - use Q key to avoid conflict with jump
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                message = self.player.use_special(current_time)
                if message:
                    print(message)  # Could show on screen
                    
        # Update player
        self.player.update(self.level.platforms, self.level.enemies, 
                          pygame.sprite.Group(), current_time)
        
        # Update level
        result = self.level.update(current_time, self.player)
        if result:
            if result[0] == 'coin':
                self.score_manager.add_score(result[1], 'coin')
            elif result[0] == 'exit':
                self.level_complete()
                
        # Check enemy bullet collisions with player
        for enemy in self.level.enemies:
            for bullet in enemy.bullets:
                if self.player.rect.colliderect(bullet.rect):
                    self.player.take_damage(bullet.damage, current_time)
                    bullet.kill()
                    
        # Check direct enemy collision
        for enemy in self.level.enemies:
            if self.player.rect.colliderect(enemy.rect):
                self.player.take_damage(10, current_time)
                
        # Update score manager
        self.score_manager.update(dt)
        
        # Update PEEL companion
        self.peel.update()
        
        # Show intro hints
        if self.game_start_timer > 0:
            self.game_start_timer -= 1
            if self.game_start_timer == 100:
                self.peel.show_hint('movement')
            elif self.game_start_timer == 60:
                self.peel.show_hint('combat')
        
        # Update keeper
        if self.current_keeper:
            self.current_keeper.update()
            # Check for rescue
            if self.current_keeper.can_interact(self.player):
                # Auto-rescue when near
                result = self.current_keeper.rescue()
                if result:
                    self.peel.show_hint('secrets')  # Celebrate!
                    # Grant keeper power to player
                    self._grant_keeper_power(result['power'])
        
        # Check player death
        if not self.player.is_alive():
            self.game_over(won=False)
            
        # Render
        self.screen.fill(JUNGLE_GREEN)  # Jungle background
        
        # Draw level
        self.level.draw(self.screen)
        
        # Draw keeper if present
        if self.current_keeper:
            self.current_keeper.draw(self.screen, self.level.camera_x)
        
        # Draw player
        self.player.draw(self.screen, self.level.camera_x)
        
        # Draw PEEL companion
        self.peel.draw(self.screen, self.player.rect.x, self.player.rect.y, self.level.camera_x)
        
        # Draw HUD
        self.hud.draw(self.screen, self.player, self.score_manager, self.current_level)
        
    def update_pause(self, events):
        """Update pause menu"""
        mouse_pos = pygame.mouse.get_pos()
        result = self.pause_menu.update(mouse_pos, events)
        
        if result == "resume":
            self.state = STATE_PLAYING
        elif result == "restart":
            self.restart_level()
        elif result == "quit":
            self.state = STATE_MENU
            
        # Draw game in background
        self.screen.fill(JUNGLE_GREEN)
        self.level.draw(self.screen)
        self.player.draw(self.screen, self.level.camera_x)
        self.hud.draw(self.screen, self.player, self.score_manager, self.current_level)
        
        # Draw pause overlay
        self.pause_menu.draw(self.screen)
        
    def update_game_over(self, events):
        """Update game over screen"""
        mouse_pos = pygame.mouse.get_pos()
        result = self.game_over_menu.update(mouse_pos, events)
        
        if result == "restart":
            self.restart_level()
        elif result == "menu":
            self.state = STATE_MENU
            
        self.game_over_menu.draw(self.screen)
        
    def update_high_scores(self, events):
        """Update high scores screen"""
        mouse_pos = pygame.mouse.get_pos()
        result = self.high_score_menu.update(mouse_pos, events)
        
        if result == "back":
            self.state = STATE_MENU
            
        self.high_score_menu.draw(self.screen)
        
    def update_level_complete(self, events):
        """Handle level completion"""
        # Move to next level or show victory
        if self.current_level < self.max_levels:
            self.current_level += 1
            self.start_level()
        else:
            self.game_over(won=True)
            
    def start_game(self):
        """Start a new game - begins at Level 0 (Tutorial)"""
        self.score_manager.reset()
        self.story_manager = StoryManager()  # Reset story
        self.peel = PEELCompanion(self.story_manager)
        self.current_level = 0
        self.game_start_timer = 120  # Show intro after 2 seconds
        self.start_level()
        
    def start_level(self):
        """Start current level"""
        # Load level data (0 = Tutorial, 1-3 = Main levels)
        levels = [LEVEL_0_DATA, LEVEL_1_DATA, LEVEL_2_DATA, LEVEL_3_DATA]
        level_data = levels[self.current_level]
        self.level = Level(level_data, self.current_level)
        
        # Create player
        start_x, start_y = self.level.player_start
        self.player = create_player(self.selected_character, start_x, start_y)
        
        # Spawn Keeper for this level (if not tutorial)
        self.current_keeper = None
        if self.current_level > 0:
            keeper_id, keeper_data = self.story_manager.get_keeper_for_level(self.current_level)
            if keeper_id and not keeper_data['rescued']:
                # Place keeper near the end of the level
                self.current_keeper = Keeper(
                    self.level.exit_rect.x - 150 if self.level.exit_rect else 800,
                    300,
                    keeper_id,
                    self.story_manager
                )
        
        # Start level timing
        self.score_manager.start_level()
        
        # PEEL shows hint for this level
        if self.current_level == 0:
            self.peel.show_hint('intro')
        elif self.current_keeper:
            self.peel.show_hint(f'keeper_{self.current_keeper.keeper_id}')
        
        self.state = STATE_PLAYING
        
    def restart_level(self):
        """Restart current level"""
        self.start_level()
        
    def level_complete(self):
        """Handle level completion"""
        # Add level completion bonus
        bonus = 1000 * self.current_level
        self.score_manager.add_level_score(self.current_level, bonus)
        
        if self.current_level < self.max_levels:
            self.current_level += 1
            self.start_level()
        else:
            self.game_over(won=True)
            
    def _grant_keeper_power(self, power_name):
        """Grant a keeper power to the player"""
        if power_name == "Fire Rounds":
            # Increase bullet damage
            self.player.damage_multiplier = 1.5
        elif power_name == "Double Jump":
            # Enable double jump
            self.player.can_double_jump = True
        elif power_name == "Shard Magnet":
            # Enable coin magnet (implemented in level update)
            self.player.has_magnet = True
            
    def game_over(self, won=False):
        """Handle game over"""
        self.game_over_menu = GameOverMenu(
            self.score_manager.get_current_score(),
            won
        )
        
        # Check and save high score
        if self.score_manager.check_high_score():
            # Could prompt for name here, using default for now
            self.score_manager.save_high_score("Player")
            
        self.state = STATE_GAME_OVER


def main():
    """Entry point"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
