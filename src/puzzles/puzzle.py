"""
Puzzle mechanics for the game
"""
import pygame
from src.constants import *


class Puzzle(pygame.sprite.Sprite):
    """Base puzzle class"""
    
    def __init__(self, x, y, width, height, puzzle_id):
        super().__init__()
        self.puzzle_id = puzzle_id
        self.solved = False
        self.activated = False
        
        self.image = pygame.Surface([width, height])
        self.image.fill(DARK_GRAY)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Activation range
        self.activate_range = 80
        
    def can_activate(self, player):
        """Check if player is close enough to activate"""
        distance = pygame.math.Vector2(
            player.rect.centerx - self.rect.centerx,
            player.rect.centery - self.rect.centery
        ).length()
        return distance < self.activate_range
        
    def activate(self):
        """Activate the puzzle"""
        self.activated = True
        
    def solve(self):
        """Mark puzzle as solved"""
        self.solved = True
        self.image.fill(GREEN)
        
    def update(self, player, keys):
        """Update puzzle state"""
        pass
        
    def draw(self, surface, camera_x=0):
        """Draw puzzle"""
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y))
        # Draw activation indicator
        if not self.solved and self.can_activate(pygame.sprite.Sprite()):
            indicator = pygame.Surface((10, 10))
            indicator.fill(YELLOW)
            surface.blit(indicator, (self.rect.centerx - 5 - camera_x, self.rect.y - 15))


class SwitchPuzzle(Puzzle):
    """Simple switch that opens doors/gates"""
    
    def __init__(self, x, y, puzzle_id, target_id):
        super().__init__(x, y, 32, 48, puzzle_id)
        self.target_id = target_id
        self.pressed = False
        # Draw switch
        self.image.fill(DARK_GRAY)
        pygame.draw.rect(self.image, GRAY, (8, 20, 16, 28))
        pygame.draw.circle(self.image, RED, (16, 16), 8)
        
    def activate(self):
        """Press the switch"""
        super().activate()
        self.pressed = True
        self.solve()
        return self.target_id


class CodePuzzle(Puzzle):
    """Enter a code sequence"""
    
    def __init__(self, x, y, puzzle_id, code="1234"):
        super().__init__(x, y, 64, 64, puzzle_id)
        self.code = code
        self.entered = ""
        self.max_digits = len(code)
        # Draw keypad base
        self._draw_keypad()
        
    def _draw_keypad(self):
        """Draw keypad interface"""
        self.image.fill(DARK_GRAY)
        # Display
        pygame.draw.rect(self.image, BLACK, (4, 4, 56, 16))
        # Buttons
        for i in range(3):
            for j in range(3):
                num = i * 3 + j + 1
                rect = pygame.Rect(6 + j * 20, 24 + i * 12, 16, 10)
                pygame.draw.rect(self.image, GRAY, rect)
                
    def update(self, player, keys):
        """Handle keypad input"""
        if not self.activated:
            return
            
        # Number keys 1-9
        for i in range(pygame.K_1, pygame.K_9 + 1):
            if keys[i]:
                self.entered += str(i - pygame.K_0)
                if len(self.entered) > self.max_digits:
                    self.entered = self.entered[-self.max_digits:]
                    
        # Check if code is correct
        if self.entered == self.code:
            self.solve()


class PressurePlate(Puzzle):
    """Pressure plate activated by standing on it"""
    
    def __init__(self, x, y, puzzle_id, target_id, weight_required=1):
        super().__init__(x, y, 48, 16, puzzle_id)
        self.target_id = target_id
        self.weight_required = weight_required
        self.weight_on = 0
        # Draw plate
        self.image.fill(DARK_GRAY)
        pygame.draw.rect(self.image, GRAY, (2, 2, 44, 12))
        
    def update(self, player, keys):
        """Check if player is standing on plate"""
        if self.rect.colliderect(player.rect):
            if player.rect.bottom <= self.rect.centery and player.vel_y >= 0:
                self.weight_on = 1
                if self.weight_on >= self.weight_required:
                    if not self.solved:
                        self.solve()
            else:
                self.weight_on = 0
        else:
            self.weight_on = 0


class Door(pygame.sprite.Sprite):
    """Door that opens when puzzle is solved"""
    
    def __init__(self, x, y, height, door_id):
        super().__init__()
        self.door_id = door_id
        self.closed = True
        
        self.image = pygame.Surface([32, height])
        self.image.fill(BROWN)
        # Add door details
        pygame.draw.rect(self.image, DARK_GRAY, (4, 4, 24, height - 8))
        pygame.draw.circle(self.image, GOLD, (20, height // 2), 4)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.closed_rect = self.rect.copy()
        
    def open(self):
        """Open the door"""
        self.closed = False
        self.rect.height = 0  # Disable collision
        self.image.set_alpha(50)  # Fade out
        
    def close(self):
        """Close the door"""
        self.closed = True
        self.rect = self.closed_rect.copy()
        self.image.set_alpha(255)
        
    def update(self, puzzle_manager):
        """Check if linked puzzle is solved"""
        if puzzle_manager.is_solved(self.door_id) and self.closed:
            self.open()


class PuzzleManager:
    """Manages all puzzles in a level"""
    
    def __init__(self):
        self.puzzles = {}
        self.doors = {}
        self.solved_ids = set()
        
    def add_puzzle(self, puzzle):
        """Add a puzzle"""
        self.puzzles[puzzle.puzzle_id] = puzzle
        
    def add_door(self, door):
        """Add a door"""
        self.doors[door.door_id] = door
        
    def update(self, player, keys):
        """Update all puzzles"""
        # Check for puzzle activation
        for puzzle in self.puzzles.values():
            if not puzzle.solved and puzzle.can_activate(player):
                if keys[pygame.K_e] or keys[pygame.K_RETURN]:
                    puzzle.activate()
                    
            puzzle.update(player, keys)
            
            if puzzle.solved and puzzle.puzzle_id not in self.solved_ids:
                self.solved_ids.add(puzzle.puzzle_id)
                # Open linked doors
                if hasattr(puzzle, 'target_id'):
                    target_id = puzzle.target_id
                    if target_id in self.doors:
                        self.doors[target_id].open()
                        
        # Update doors
        for door in self.doors.values():
            door.update(self)
            
    def is_solved(self, puzzle_id):
        """Check if a puzzle is solved"""
        return puzzle_id in self.solved_ids
        
    def draw(self, surface, camera_x=0):
        """Draw all puzzles and doors"""
        for puzzle in self.puzzles.values():
            puzzle.draw(surface, camera_x)
        for door in self.doors.values():
            surface.blit(door.image, (door.rect.x - camera_x, door.rect.y))
