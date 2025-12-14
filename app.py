
from flask import Flask, request, jsonify
from models import Room, Player, Game
import database as db
import game_logic as logic
from datetime import datetime

app = Flask(__name__)

@app.route('/room/create', methods=['POST'])
def create_room():

    data = request.get_json()
    
    if not data or 'player_name' not in data:
        return jsonify({'error': 'player_name is required'}), 400
    
    player_name = data['player_name']

    room = Room(
        room_id='',
        created_by='',
        status='waiting',
        player_count=1
    )
    
    player = Player(
        player_id='',
        name=player_name,
        room_id=''
    )
    
    room = db.create_room(room)
    player.room_id = room.room_id
    room.created_by = player.player_id
    player = db.add_player(player)
    

    room.created_by = player.player_id
    db.update_room(room)
    
    return jsonify({
        'room_id': room.room_id,
        'player_id': player.player_id,
        'player_name': player.name,
        'message': 'Room created successfully',
        'players_joined': 1,
        'waiting_for': 3
    }), 201


@app.route('/room/join', methods=['POST'])
def join_room():

    data = request.get_json()
    
    if not data or 'room_id' not in data or 'player_name' not in data:
        return jsonify({'error': 'room_id and player_name are required'}), 400
    
    room_id = data['room_id']
    player_name = data['player_name']
    
    room = db.get_room(room_id)
    if not room:
        return jsonify({'error': 'Room not found'}), 404
    current_players = db.get_players_in_room(room_id)
    if len(current_players) >= 4:
        return jsonify({'error': 'Room is full'}), 400
  
    if room.status != 'waiting':
        return jsonify({'error': 'Game already started'}), 400
    

    player = Player(
        player_id='',
        name=player_name,
        room_id=room_id
    )
    player = db.add_player(player)
    

    room.player_count = len(current_players) + 1
    db.update_room(room)
    
    response = {
        'player_id': player.player_id,
        'player_name': player.name,
        'room_id': room_id,
        'message': 'Joined room successfully',
        'players_joined': room.player_count,
        'waiting_for': 4 - room.player_count
    }
    
    if room.player_count == 4:
        response['message'] = 'Joined room successfully. All players ready! Assigning roles...'
    
        assign_roles_internal(room_id)
    
    return jsonify(response), 200


@app.route('/room/players/<room_id>', methods=['GET'])
def get_room_players(room_id):

    room = db.get_room(room_id)
    if not room:
        return jsonify({'error': 'Room not found'}), 404
    
    players = db.get_players_in_room(room_id)
    
    return jsonify({
        'room_id': room_id,
        'status': room.status,
        'player_count': len(players),
        'players': [p.to_public_dict() for p in players]
    }), 200

def assign_roles_internal(room_id):
    room = db.get_room(room_id)
    players = db.get_players_in_room(room_id)
    
    if len(players) != 4:
        return False
    players = logic.assign_roles(players)
    db.update_players_batch(players)

    room.status = 'playing'
    db.update_room(room)

    mantri = logic.get_mantri_player(players)
    chor = logic.get_chor_player(players)
    
    game = Game(
        game_id='',
        room_id=room_id,
        mantri_player_id=mantri.player_id,
        chor_player_id=chor.player_id,
        status='in_progress'
    )
    db.create_game(game)
    
    return True


@app.route('/room/assign/<room_id>', methods=['POST'])
def assign_roles(room_id):
    room = db.get_room(room_id)
    if not room:
        return jsonify({'error': 'Room not found'}), 404
    
    players = db.get_players_in_room(room_id)
    
    if len(players) != 4:
        return jsonify({'error': 'Need exactly 4 players to start game'}), 400
    
    if room.status != 'waiting':
        return jsonify({'error': 'Roles already assigned'}), 400
    
    success = assign_roles_internal(room_id)
    
    if success:
        return jsonify({
            'message': 'Roles assigned successfully',
            'room_id': room_id,
            'status': 'playing'
        }), 200
    else:
        return jsonify({'error': 'Failed to assign roles'}), 500
@app.route('/role/me/<room_id>/<player_id>', methods=['GET'])
def get_my_role(room_id, player_id):

    room = db.get_room(room_id)
    if not room:
        return jsonify({'error': 'Room not found'}), 404
    
    player = db.get_player(player_id)
    if not player:
        return jsonify({'error': 'Player not found'}), 404
    
    if player.room_id != room_id:
        return jsonify({'error': 'Player not in this room'}), 403
    
    if not player.role:
        return jsonify({'error': 'Roles not yet assigned. Waiting for players...'}), 400
    
    return jsonify({
        'player_id': player.player_id,
        'name': player.name,
        'role': player.role,
        'description': get_role_description(player.role)
    }), 200


def get_role_description(role):
    descriptions = {
        'Raja': 'You are the Raja (King). Observe and wait for results. You get 1000 points.',
        'Mantri': 'You are the Mantri (Minister). You must guess who the Chor is!',
        'Chor': 'You are the Chor (Thief). Try not to get caught!',
        'Sipahi': 'You are the Sipahi (Soldier). Wait for Mantri to make their guess.'
    }
    return descriptions.get(role, '')
@app.route('/guess/<room_id>', methods=['POST'])
def submit_guess(room_id):

    data = request.get_json()
    
    if not data or 'mantri_player_id' not in data or 'guessed_player_id' not in data:
        return jsonify({'error': 'mantri_player_id and guessed_player_id are required'}), 400
    
    mantri_player_id = data['mantri_player_id']
    guessed_player_id = data['guessed_player_id']
    
    # Validate room
    room = db.get_room(room_id)
    if not room:
        return jsonify({'error': 'Room not found'}), 404
    
    if room.status != 'playing':
        return jsonify({'error': 'Game not in progress'}), 400
    
    mantri = db.get_player(mantri_player_id)
    if not mantri or mantri.room_id != room_id:
        return jsonify({'error': 'Invalid mantri player'}), 403
    
    if mantri.role != 'Mantri':
        return jsonify({'error': 'Only Mantri can submit guess'}), 403
    

    guessed_player = db.get_player(guessed_player_id)
    if not guessed_player or guessed_player.room_id != room_id:
        return jsonify({'error': 'Invalid guessed player'}), 400
    players = db.get_players_in_room(room_id)
    game = db.get_current_game(room_id)
    
    if not game:
        return jsonify({'error': 'No active game found'}), 404
    

    chor = logic.get_chor_player(players)
    scores, guess_correct = logic.calculate_scores(mantri, guessed_player_id, chor)
    
  
    game.guessed_player_id = guessed_player_id
    game.guess_correct = guess_correct
    game.raja_points = scores['Raja']
    game.mantri_points = scores['Mantri']
    game.chor_points = scores['Chor']
    game.sipahi_points = scores['Sipahi']
    game.status = 'completed'
    db.update_game(game)
    
    # Update player scores
    players = logic.update_player_scores(players, scores)
    db.update_players_batch(players)

    room.status = 'finished'
    db.update_room(room)
    result = logic.prepare_game_result(players, game)
    
    return jsonify({
        'message': 'Guess submitted successfully',
        'result': result
    }), 200

@app.route('/result/<room_id>', methods=['GET'])
def get_result(room_id):
    room = db.get_room(room_id)
    if not room:
        return jsonify({'error': 'Room not found'}), 404
    
    if room.status != 'finished':
        return jsonify({'error': 'Game not yet finished'}), 400
    
    players = db.get_players_in_room(room_id)
    game = db.get_current_game(room_id)
    
    if not game or game.status != 'completed':
        return jsonify({'error': 'No completed game found'}), 404
    
    result = logic.prepare_game_result(players, game)
    
    return jsonify(result), 200

@app.route('/leaderboard/<room_id>', methods=['GET'])
def get_leaderboard(room_id):
    room = db.get_room(room_id)
    if not room:
        return jsonify({'error': 'Room not found'}), 404
    
    players = db.get_players_in_room(room_id)
    players.sort(key=lambda p: p.points, reverse=True)
    
    leaderboard = []
    for rank, player in enumerate(players, 1):
        leaderboard.append({
            'rank': rank,
            'player_id': player.player_id,
            'name': player.name,
            'total_points': player.points
        })
    
    return jsonify({
        'room_id': room_id,
        'leaderboard': leaderboard
    }), 200
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'Raja-Mantri-Chor-Sipahi Backend is running',
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route("/health", methods=["GET"])
def health():
    return {
        "status": "healthy",
        "message": "Raja-Mantri-Chor-Sipahi Backend is running"
    }
if __name__ == '__main__':
    print("🎮 Raja-Mantri-Chor-Sipahi Backend Starting...")
    print("📝 Database initialized at ./data/")
    print("🚀 Server running on http://localhost:5000")

    app.run(debug=True, host='0.0.0.0', port=5000) 
