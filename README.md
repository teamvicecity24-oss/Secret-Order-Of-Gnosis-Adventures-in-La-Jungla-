# Secret Order of Gnosis: Adventures in La Jungla

A 2D platformer shooter game built with Pygame featuring 5 unique playable characters, enemy AI, puzzles, and multiple levels.

## Features

### 5 Playable Characters

Each character has unique stats and a special ability:

1. **Recon** (Cyan)
   - Fastest movement speed
   - Rapid fire weapon
   - **Special:** Speed Boost - Doubles speed and firing rate for 3 seconds

2. **Heavy** (Red)
   - High health pool (150 HP)
   - Slow but powerful
   - **Special:** Explosive Round - Fires a massive explosive projectile

3. **Tech** (Blue)
   - Balanced stats
   - **Special:** Energy Shield - Absorbs one hit without taking damage

4. **Medic** (Green)
   - Support-focused
   - **Special:** Heal Pulse - Restores 30 health instantly

5. **Stealth** (Purple)
   - Fast and stealthy
   - Higher damage when cloaked
   - **Special:** Cloak - Become invisible to enemies for 4 seconds

### Gameplay

- **Platforming:** Jump across platforms, avoid hazards
- **Shooting:** Defeat enemies with your weapon (Ctrl or F)
- **Special Abilities:** Press Q to activate your character's special
- **Puzzles:** Solve switch puzzles and pressure plates to progress
- **Multiple Levels:** 3 unique levels with increasing difficulty
- **High Scores:** Compete for the best score with time bonuses

### Enemies

- **Patrol Enemy:** Moves back and forth, chases when player is near
- **Turret:** Stationary, shoots at player in range
- **Flying Enemy:** Doesn't obey gravity, hovers and shoots
- **Boss:** Multi-phase boss with complex attack patterns

### Controls

| Key | Action |
|-----|--------|
| A / D or ← / → | Move left/right |
| W or ↑ | Jump |
| Ctrl or F | Shoot |
| Q | Special Ability |
| E | Interact with puzzles |
| ESC | Pause |

## Installation

### Requirements
- Python 3.8+
- Pygame 2.5.0+

### Setup

1. Clone or download the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Run the game:
```bash
python main.py
```

## Project Structure

```
pygame-project/
├── main.py                 # Game entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── src/                   # Source code
│   ├── constants.py       # Game constants
│   ├── sprite.py          # Base sprite class
│   ├── scoring.py         # Score manager
│   ├── characters/        # Player characters
│   │   └── player.py
│   ├── enemies/           # Enemy classes
│   │   └── enemy.py
│   ├── levels/            # Level system
│   │   ├── level.py
│   │   └── collectible.py
│   ├── puzzles/           # Puzzle mechanics
│   │   └── puzzle.py
│   ├── weapons/           # Weapons and bullets
│   │   └── bullet.py
│   └── ui/                # UI and menus
│       └── menu.py
└── assets/               # Game assets (images, sounds)
    ├── images/
    ├── sounds/
    └── music/
```

## How to Push to GitHub

1. Initialize git repository:
```bash
git init
```

2. Add all files:
```bash
git add .
```

3. Commit:
```bash
git commit -m "Initial commit: Secret Order of Gnosis game"
```

4. Add your GitHub remote (use your referral link):
```bash
git remote add origin https://github.com/YOUR_USERNAME/secret-order-of-gnosis.git
```

5. Push:
```bash
git push -u origin main
```

## Future Enhancements

- Add sound effects and music
- Create more levels
- Add more enemy types
- Implement multiplayer co-op
- Add story/cutscenes
- Create custom artwork
- Add save/load system
- Power-ups and upgrades

## Credits

Built with Pygame - Python game development library

## License

MIT License - Feel free to use and modify!
