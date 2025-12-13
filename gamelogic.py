"""
game_logic.py
-------------
Contains core game logic for role assignment, scoring, and game flow.
"""

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
    """
    Randomly assign roles to 4 players.
    Returns updated player list with roles assigned.
    """
    if len(players) != 4:
        raise ValueError("Exactly 4 players required for role assignment")
    
    # Shuffle roles and assign
    shuffled_roles = random.sample(ROLES, len(ROLES))
    
    for i, player in enumerate(players):
        player.role = shuffled_roles[i]
        player.points = 0  # Reset points for new game
    
    return players


def calculate_scores(mantri_player: Player, guessed_player_id: str, 
                     chor_player: Player) -> Tuple[Dict[str, int], bool]:
    """
    Calculate scores based on Mantri's guess.
    
    Returns:
        - Dictionary of role -> points
        - Boolean indicating if guess was correct
    """
    guess_correct = (guessed_player_id == chor_player.player_id)
    
    if guess_correct:
        # Mantri guessed correctly
        # Mantri and Sipahi keep their points, Chor gets 0
        scores = {
            'Raja': DEFAULT_POINTS['Raja'],
            'Mantri': DEFAULT_POINTS['Mantri'],
            'Chor': DEFAULT_POINTS['Chor'],
            'Sipahi': DEFAULT_POINTS['Sipahi']
        }
    else:
        # Mantri guessed wrong
        # Chor steals Mantri's and Sipahi's points
        stolen_points = DEFAULT_POINTS['Mantri'] + DEFAULT_POINTS['Sipahi']
        scores = {
            'Raja': DEFAULT_POINTS['Raja'],
            'Mantri': 0,
            'Chor': stolen_points,
            'Sipahi': 0
        }
    
    return scores, guess_correct


def update_player_scores(players: List[Player], scores: Dict[str, int]) -> List[Player]:
    """
    Update player points based on calculated scores.
    Adds points to cumulative totals.
    """
    for player in players:
        if player.role in scores:
            player.points += scores[player.role]
    
    return players


def get_mantri_player(players: List[Player]) -> Player:
    """Get the player with Mantri role"""
    for player in players:
        if player.role == 'Mantri':
            return player
    raise ValueError("No Mantri found in players")


def get_chor_player(players: List[Player]) -> Player:
    """Get the player with Chor role"""
    for player in players:
        if player.role == 'Chor':
            return player
    raise ValueError("No Chor found in players")


def get_player_by_role(players: List[Player], role: str) -> Player:
    """Get player by their role"""
    for player in players:
        if player.role == role:
            return player
    return None


def prepare_game_result(players: List[Player], game: Game) -> Dict:
    """
    Prepare the final game result to be returned to players.
    Includes all roles revealed and final scores.
    """
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