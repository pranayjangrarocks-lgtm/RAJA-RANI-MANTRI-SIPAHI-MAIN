
import csv
import os
from typing import List, Optional
from models import Room, Player, Game
import threading
csv_lock = threading.Lock()

DATA_DIR = 'data'
ROOMS_FILE = os.path.join(DATA_DIR, 'rooms.csv')
PLAYERS_FILE = os.path.join(DATA_DIR, 'players.csv')
GAMES_FILE = os.path.join(DATA_DIR, 'games.csv')

def init_database():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(ROOMS_FILE):
        with open(ROOMS_FILE, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['room_id', 'created_by', 'status', 'player_count', 'created_at'])
            writer.writeheader()
    if not os.path.exists(PLAYERS_FILE):
        with open(PLAYERS_FILE, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['player_id', 'name', 'room_id', 'role', 'points', 'joined_at'])
            writer.writeheader()
    if not os.path.exists(GAMES_FILE):
        with open(GAMES_FILE, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'game_id', 'room_id', 'mantri_player_id', 'guessed_player_id', 
                'chor_player_id', 'guess_correct', 'raja_points', 'mantri_points', 
                'chor_points', 'sipahi_points', 'status', 'created_at'
            ])
            writer.writeheader()
def create_room(room: Room) -> Room:
    """Create a new room"""
    with csv_lock:
        with open(ROOMS_FILE, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=room.to_dict().keys())
            writer.writerow(room.to_dict())
    return room


def get_room(room_id: str) -> Optional[Room]:
    import csv
    import os
    from typing import List, Optional
    from models import Room, Player, Game
    import threading

    csv_lock = threading.Lock()

    DATA_DIR = 'data'
    ROOMS_FILE = os.path.join(DATA_DIR, 'rooms.csv')
    PLAYERS_FILE = os.path.join(DATA_DIR, 'players.csv')
    GAMES_FILE = os.path.join(DATA_DIR, 'games.csv')

    def init_database():
        os.makedirs(DATA_DIR, exist_ok=True)
        if not os.path.exists(ROOMS_FILE):
            with open(ROOMS_FILE, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['room_id', 'created_by', 'status', 'player_count', 'created_at'])
                writer.writeheader()
        if not os.path.exists(PLAYERS_FILE):
            with open(PLAYERS_FILE, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['player_id', 'name', 'room_id', 'role', 'points', 'joined_at'])
                writer.writeheader()
        if not os.path.exists(GAMES_FILE):
            with open(GAMES_FILE, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    'game_id', 'room_id', 'mantri_player_id', 'guessed_player_id', 
                    'chor_player_id', 'guess_correct', 'raja_points', 'mantri_points', 
                    'chor_points', 'sipahi_points', 'status', 'created_at'
                ])
                writer.writeheader()

    def create_room(room: Room) -> Room:
        with csv_lock:
            with open(ROOMS_FILE, 'a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=room.to_dict().keys())
                writer.writerow(room.to_dict())
        return room

    def get_room(room_id: str) -> Optional[Room]:
        import csv
        import os
        from typing import List, Optional
        from models import Room, Player, Game
        import threading
        csv_lock = threading.Lock()

        DATA_DIR = 'data'
        ROOMS_FILE = os.path.join(DATA_DIR, 'rooms.csv')
        PLAYERS_FILE = os.path.join(DATA_DIR, 'players.csv')
        GAMES_FILE = os.path.join(DATA_DIR, 'games.csv')

        def init_database():
            os.makedirs(DATA_DIR, exist_ok=True)
            if not os.path.exists(ROOMS_FILE):
                with open(ROOMS_FILE, 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=['room_id', 'created_by', 'status', 'player_count', 'created_at'])
                    writer.writeheader()
            if not os.path.exists(PLAYERS_FILE):
                with open(PLAYERS_FILE, 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=['player_id', 'name', 'room_id', 'role', 'points', 'joined_at'])
                    writer.writeheader()
 
            if not os.path.exists(GAMES_FILE):
                with open(GAMES_FILE, 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=[
                        'game_id', 'room_id', 'mantri_player_id', 'guessed_player_id', 
                        'chor_player_id', 'guess_correct', 'raja_points', 'mantri_points', 
                        'chor_points', 'sipahi_points', 'status', 'created_at'
                    ])
                    writer.writeheader()

        def create_room(room: Room) -> Room:
            with csv_lock:
                with open(ROOMS_FILE, 'a', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=room.to_dict().keys())
                    writer.writerow(room.to_dict())
            return room


        def get_room(room_id: str) -> Optional[Room]:
            with csv_lock:
                with open(ROOMS_FILE, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if row['room_id'] == room_id:
                            return Room(**row)
            return None


        def update_room(room: Room):
            with csv_lock:
                rows = []
                with open(ROOMS_FILE, 'r') as f:
                    reader = csv.DictReader(f)
                    rows = list(reader)
        
                with open(ROOMS_FILE, 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=rows[0].keys() if rows else room.to_dict().keys())
                    writer.writeheader()
                    for row in rows:
                        if row['room_id'] == room.room_id:
                            writer.writerow(room.to_dict())
                        else:
                            writer.writerow(row)

        def add_player(player: Player) -> Player:
            with csv_lock:
                with open(PLAYERS_FILE, 'a', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=player.to_dict().keys())
                    writer.writerow(player.to_dict())
            return player


        def get_players_in_room(room_id: str) -> List[Player]:
 
            players = []
            with csv_lock:
                with open(PLAYERS_FILE, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if row['room_id'] == room_id:
                            row['points'] = int(row['points']) if row['points'] else 0
                            players.append(Player(**row))
            return players


        def get_player(player_id: str) -> Optional[Player]:
            with csv_lock:
                with open(PLAYERS_FILE, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if row['player_id'] == player_id:
                            row['points'] = int(row['points']) if row['points'] else 0
                            return Player(**row)
            return None


        def update_player(player: Player):
            with csv_lock:
                rows = []
                with open(PLAYERS_FILE, 'r') as f:
                    reader = csv.DictReader(f)
                    rows = list(reader)
        
                with open(PLAYERS_FILE, 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=rows[0].keys() if rows else player.to_dict().keys())
                    writer.writeheader()
                    for row in rows:
                        if row['player_id'] == player.player_id:
                            writer.writerow(player.to_dict())
                        else:
                            writer.writerow(row)


        def update_players_batch(players: List[Player]):
            with csv_lock:
                rows = []
                player_dict = {p.player_id: p for p in players}
        
                with open(PLAYERS_FILE, 'r') as f:
                    reader = csv.DictReader(f)
                    rows = list(reader)
        
                with open(PLAYERS_FILE, 'w', newline='') as f:
                    if rows:
                        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                    else:
                        writer = csv.DictWriter(f, fieldnames=players[0].to_dict().keys())
                    writer.writeheader()
                    for row in rows:
                        if row['player_id'] in player_dict:
                            writer.writerow(player_dict[row['player_id']].to_dict())
                        else:
                            writer.writerow(row)

        def create_game(game: Game) -> Game:
            with csv_lock:
                with open(GAMES_FILE, 'a', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=game.to_dict().keys())
                    writer.writerow(game.to_dict())
            return game


        def get_current_game(room_id: str) -> Optional[Game]:
            
            with csv_lock:
                with open(GAMES_FILE, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if row['room_id'] == room_id and row['status'] == 'in_progress':
                            # Convert numeric fields
                            for key in ['raja_points', 'mantri_points', 'chor_points', 'sipahi_points']:
                                row[key] = int(row[key]) if row[key] else 0
                            row['guess_correct'] = row['guess_correct'] == 'True' if row['guess_correct'] else None
                            return Game(**row)
            return None


        def update_game(game: Game):
            
            with csv_lock:
                rows = []
                with open(GAMES_FILE, 'r') as f:
                    reader = csv.DictReader(f)
                    rows = list(reader)
        
                with open(GAMES_FILE, 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=rows[0].keys() if rows else game.to_dict().keys())
                    writer.writeheader()
                    for row in rows:
                        if row['game_id'] == game.game_id:
                            writer.writerow(game.to_dict())
                        else:

                            writer.writerow(row)
