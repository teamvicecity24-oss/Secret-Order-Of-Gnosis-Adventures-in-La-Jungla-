"""
Score and high score system
"""
import json
import os
from src.constants import *


class ScoreManager:
    """Manages game scoring and high scores"""
    
    def __init__(self):
        self.current_score = 0
        self.high_scores = []
        self.coins_collected = 0
        self.enemies_defeated = 0
        self.level_scores = {}  # Score per level
        self.total_time = 0
        self.level_time = 0
        
        # File path for saving scores
        self.score_file = "highscores.json"
        
        # Load existing high scores
        self.load_high_scores()
        
    def add_score(self, points, source=""):
        """Add points to current score"""
        self.current_score += points
        
        # Track by source
        if source == "enemy":
            self.enemies_defeated += 1
        elif source == "coin":
            self.coins_collected += points // 100
            
    def add_level_score(self, level_number, bonus=0):
        """Add level completion bonus"""
        # Time bonus - faster = more points
        time_bonus = max(0, 10000 - self.level_time * 10)
        level_total = bonus + time_bonus
        self.current_score += level_total
        self.level_scores[level_number] = level_total
        
    def start_level(self):
        """Start timing a level"""
        self.level_time = 0
        
    def update(self, dt):
        """Update timers"""
        self.level_time += dt
        self.total_time += dt
        
    def get_current_score(self):
        """Get current score"""
        return self.current_score
        
    def get_high_scores(self, limit=10):
        """Get top high scores"""
        return sorted(self.high_scores, key=lambda x: x['score'], reverse=True)[:limit]
        
    def check_high_score(self):
        """Check if current score is a high score"""
        scores = self.get_high_scores()
        if len(scores) < 10:
            return True
        return self.current_score > scores[-1]['score']
        
    def save_high_score(self, player_name):
        """Save current score as high score"""
        score_entry = {
            'name': player_name,
            'score': self.current_score,
            'enemies': self.enemies_defeated,
            'coins': self.coins_collected,
            'time': self.total_time,
            'date': self._get_date()
        }
        self.high_scores.append(score_entry)
        self.save_high_scores()
        
    def reset(self):
        """Reset current game score"""
        self.current_score = 0
        self.coins_collected = 0
        self.enemies_defeated = 0
        self.level_scores = {}
        self.total_time = 0
        self.level_time = 0
        self.start_level()
        
    def load_high_scores(self):
        """Load high scores from file"""
        if os.path.exists(self.score_file):
            try:
                with open(self.score_file, 'r') as f:
                    self.high_scores = json.load(f)
            except:
                self.high_scores = []
        else:
            self.high_scores = [
                {'name': 'Commander', 'score': 50000, 'enemies': 100, 'coins': 50, 'time': 600, 'date': '2024-01-01'},
                {'name': 'Lieutenant', 'score': 30000, 'enemies': 75, 'coins': 30, 'time': 900, 'date': '2024-01-01'},
                {'name': 'Sergeant', 'score': 15000, 'enemies': 50, 'coins': 20, 'time': 1200, 'date': '2024-01-01'},
            ]
            self.save_high_scores()
            
    def save_high_scores(self):
        """Save high scores to file"""
        with open(self.score_file, 'w') as f:
            json.dump(self.high_scores, f, indent=2)
            
    def _get_date(self):
        """Get current date string"""
        import datetime
        return datetime.datetime.now().strftime('%Y-%m-%d')
        
    def get_stats(self):
        """Get game statistics"""
        return {
            'score': self.current_score,
            'enemies': self.enemies_defeated,
            'coins': self.coins_collected,
            'time': int(self.total_time),
            'levels_completed': len(self.level_scores)
        }
