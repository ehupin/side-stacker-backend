from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, emit, join_room
import uuid, pprint
import matrix_utils

app = Flask(__name__, template_folder='static')
app.config['SECRET_KEY'] = 'thisIsSecret'
socketio = SocketIO(app, cors_allowed_origins="*", async_handlers=True)


class Player():
    def __init__(self, session_id):
        self.session_id = session_id

class Game():
    max_players = 2
    matrix_size = 7
    def __init__(self):
        self.id = uuid.uuid4().hex
        self.players = []
        self.matrix = [[None]*self.matrix_size for i in range(self.matrix_size)]

    def add_player(self, player):
        self.players.append(player)

    def is_full(self):
        return len(self.players) == self.max_players

    def add_piece(self, player, row_index, side):
        player_index = self.players.index(player)

        # find next available column in given row
        row = self.matrix[row_index]
        try:
            if side == 0:
                column_index = row.index(None)
            else:
                column_index = len(row) - row[::-1].index(None) - 1
        except ValueError as e:
            column_index = None

        # check for winning or draw
        game_is_won = game_is_draw = False
        if column_index is not None:
            row[column_index] = player_index
            game_is_won = matrix_utils.matrix_has_line(self.matrix, player_index, row_index, column_index, 4)
            if not game_is_won:
                game_is_draw = not matrix_utils.matrix_has_value(self.matrix, None)

        # notify game players for new piece added
        emit('piece_added',
             dict(row=row_index,
                  column=column_index,
                  player_id=player_index,
                  game_is_won=game_is_won,
                  game_is_draw=game_is_draw),
             room=self.id)


GAMES = []

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def on_connection():
    player = Player(request.sid)

    # found or create a game to join
    open_games = [g for g in GAMES if not g.is_full()]
    if open_games:
        player_id = 1
        game = open_games[0]
    else:
        player_id = 0
        game = Game()
        GAMES.append(game)

    # add player to game
    game.add_player(player)
    join_room(game.id)

    # store game and player info in session
    session['GAME'] = game
    session['PLAYER'] = player

    # notify game players (included the new one) for new player in game
    data = dict(game_id=game.id,
                player_id=player_id,
                game_is_full=game.is_full(),
                game_matrix_size=game.matrix_size)
    emit('player_joined_game', data, room=game.id)


@socketio.on('add_piece')
def on_piece_added(data):
    game = session.get('GAME')
    player = session.get('PLAYER')
    game.add_piece(player, data['rowIndex'], data['side'])



if __name__ == "__main__":
    socketio.run(app, debug=True)