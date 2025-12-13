"""
models.py
---------
Defines data structures for Room, Player, and Game.
These classes represent the core entities in the game.
"""

from dataclasses import dataclass, asdict
from typing import Optional, List
from datetime import datetime
import uuid

@dataclass
class Player:
    """Represents a player in the game"""
    player_id: str
    name: str
    room_id: str
    role: Optional[str] = None  # 'Raja', 'Mantri', 'Chor', 'Sipahi'
    points: int = 0
    joined_at: str = None
    
    def __post_init__(self):
        if not self.player_id:
            self.player_id = str(uuid.uuid4())
        if not self.joined_at:
            self.joined_at = datetime.now().isoformat()
    
    def to_dict(self):
        return asdict(self)
    
    def to_public_dict(self):
        """Returns player info without sensitive data (role)"""
        return {
            'player_id': self.player_id,
            'name': self.name,
            'points': self.points
        }


@dataclass
class Room:
    """Represents a game room"""
    room_id: str
    created_by: str  # player_id
    status: str = 'waiting'  # 'waiting', 'playing', 'finished'
    player_count: int = 0
    created_at: str = None
    
    def __post_init__(self):
        if not self.room_id:
            self.room_id = str(uuid.uuid4())[:8]  # Short room ID
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
    
    def to_dict(self):
        return asdict(self)


@dataclass
class Game:
    """Represents a game round with results"""
    game_id: str
    room_id: str
    mantri_player_id: str
    guessed_player_id: Optional[str] = None
    chor_player_id: Optional[str] = None
    guess_correct: Optional[bool] = None
    raja_points: int = 0
    mantri_points: int = 0
    chor_points: int = 0
    sipahi_points: int = 0
    status: str = 'in_progress'  # 'in_progress', 'completed'
    created_at: str = None
    
    def __post_init__(self):
        if not self.game_id:
            self.game_id = str(uuid.uuid4())
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
    
    def to_dict(self):
        return asdict(self)