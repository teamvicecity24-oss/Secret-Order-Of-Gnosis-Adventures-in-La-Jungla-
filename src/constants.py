"""
Secret Order of Gnosis: Adventures in La Jungla
Game Constants and Configuration
"""
import pygame

# Screen Settings
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FPS = 60
TITLE = "Secret Order of Gnosis: Adventures in La Jungla"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
BROWN = (139, 69, 19)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
GOLD = (255, 215, 0)
JUNGLE_GREEN = (34, 139, 34)

# Physics
GRAVITY = 0.8
FRICTION = 0.85
AIR_RESISTANCE = 0.95

# Player Settings
PLAYER_SPEED = 6
PLAYER_JUMP_STRENGTH = 15
PLAYER_MAX_HEALTH = 100
PLAYER_INVINCIBILITY_TIME = 1000  # milliseconds

# Shooting
BULLET_SPEED = 12
BULLET_COOLDOWN = 200  # milliseconds between shots

# Tile Settings
TILE_SIZE = 32

# Game States
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_PAUSE = "pause"
STATE_GAME_OVER = "game_over"
STATE_LEVEL_COMPLETE = "level_complete"
STATE_CHARACTER_SELECT = "character_select"

# Character Types
CHARACTER_RECON = "recon"
CHARACTER_HEAVY = "heavy"
CHARACTER_TECH = "tech"
CHARACTER_MEDIC = "medic"
CHARACTER_STEALTH = "stealth"

# Enemy Types
ENEMY_PATROL = "patrol"
ENEMY_TURRET = "turret"
ENEMY_FLYING = "flying"
ENEMY_BOSS = "boss"
