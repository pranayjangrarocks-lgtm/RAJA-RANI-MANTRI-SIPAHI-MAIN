
import random
from typing import List, Dict, Tuple
from models import Player, Game

ROLES = ['Raja', 'Mantri', 'Chor', 'Sipahi']

DEFAULT_POINTS = {
    'Raja': 1000,
    'Mantri': 800,
    'Chor': 0,
    'Sipahi': 500
}


def assign_roles(players: List[Player]) -> List[Player]:
    if len(players) != 4:
        raise ValueError("Exactly 4 players required for role assignment")
    shuffled_roles = random.sample(ROLES, len(ROLES))
    
    for i, player in enumerate(players):
        player.role = shuffled_roles[i]
        player.points = 0  
    
    return players


def calculate_scores(mantri_player: Player, guessed_player_id: str, 
                     chor_player: Player) -> Tuple[Dict[str, int], bool]:
    guess_correct = (guessed_player_id == chor_player.player_id)
    
    if guess_correct:
      
        scores = {
            'Raja': DEFAULT_POINTS['Raja'],
            'Mantri': DEFAULT_POINTS['Mantri'],
            'Chor': DEFAULT_POINTS['Chor'],
            'Sipahi': DEFAULT_POINTS['Sipahi']
        }
    else:
        stolen_points = DEFAULT_POINTS['Mantri'] + DEFAULT_POINTS['Sipahi']
        scores = {
            'Raja': DEFAULT_POINTS['Raja'],
            'Mantri': 0,
            'Chor': stolen_points,
            'Sipahi': 0
        }
    
    return scores, guess_correct


def update_player_scores(players: List[Player], scores: Dict[str, int]) -> List[Player]:
    for player in players:
        if player.role in scores:
            player.points += scores[player.role]
    
    return players


def get_mantri_player(players: List[Player]) -> Player:
    for player in players:
        if player.role == 'Mantri':
            return player
    raise ValueError("No Mantri found in players")


def get_chor_player(players: List[Player]) -> Player:
    for player in players:
        if player.role == 'Chor':
            return player
    raise ValueError("No Chor found in players")


def get_player_by_role(players: List[Player], role: str) -> Player:
    for player in players:
        if player.role == role:
            return player
    return None


def prepare_game_result(players: List[Player], game: Game) -> Dict:
    result = {
        'game_id': game.game_id,
        'mantri_guess_correct': game.guess_correct,
        'players': []
    }
    
    for player in players:
        result['players'].append({
            'player_id': player.player_id,
            'name': player.name,
            'role': player.role,
            'round_points': {
                'Raja': game.raja_points,
                'Mantri': game.mantri_points,
                'Chor': game.chor_points,
                'Sipahi': game.sipahi_points
            }[player.role],
            'total_points': player.points
        })
    

    return result
