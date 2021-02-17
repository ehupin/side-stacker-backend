from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, emit, join_room
import uuid, pprint, random, enum
import matrix_utils


app = Flask(__name__, template_folder='static')
app.config['SECRET_KEY'] = 'thisIsSecret'
socketio = SocketIO(app, cors_allowed_origins="*", async_handlers=True)


class GameMode(enum.Enum):
    one_player = 0
    two_players = 1

class GameStatus(enum.Enum):
    open = 0
    started = 1
    finished = 2

class Player():
    def __init__(self, session_id=None):
        self.session_id = session_id

class Game():
    max_players = 2
    matrix_size = 7
    def __init__(self):
        self.id = uuid.uuid4().hex
        self.players = []
        self.status = GameStatus.open.value
        self.matrix = [[None]*self.matrix_size for i in range(self.matrix_size)]

    def add_player(self, player):
        self.players.append(player)

    def is_full(self):
        is_full = len(self.players) == self.max_players
        if is_full:
            self.status = GameStatus.started.value
        return is_full

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

        if game_is_won or game_is_draw:
            self.status = GameStatus.finished.value

        # notify game players for new piece added
        emit('piece_added',
             dict(row=row_index,
                  column=column_index,
                  player_id=player_index,
                  game_is_won=game_is_won,
                  game_is_draw=game_is_draw),
             room=self.id)

class OnePlayerGame(Game):
    def add_player(self, *args, **kwargs):
        super(OnePlayerGame, self).add_player(*args,)
        super(OnePlayerGame, self).add_player(Player())

    def add_piece(self, *args, auto_play=True, **kwargs):
        super(OnePlayerGame, self).add_piece( *args, **kwargs)
        if auto_play and self.status != GameStatus.finished.value:
            self.auto_play()

    def auto_play(self):
        """ Basic auto play, add coin to the first available row on the left side
        """
        row_indexes = list(range(len(self.matrix)))
        random.shuffle(row_indexes)
        for row_index in row_indexes:
            if None in self.matrix[row_index]:
                side = random.randint(0, 1)
                self.add_piece(self.players[1], row_index, side, auto_play=False)
                return

class TwoPlayersGame(Game):
    pass

TWO_PLAYERS_GAMES = []

@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('join')
def on_join(data):
    player = Player(request.sid)

    game = None
    game_mode = data['gameMode']


    # found or create a game to join if two players mode
    if game_mode == GameMode.two_players.value:
        open_games = [g for g in TWO_PLAYERS_GAMES if not g.is_full()]
        if open_games:
            player_id = 1
            game = open_games[0]

    # if there is no open game (always true in one player mode)

    if not game:
        player_id = 0
        if game_mode == GameMode.one_player.value:
            game = OnePlayerGame()
        elif game_mode == GameMode.two_players.value:
            game = TwoPlayersGame()
            TWO_PLAYERS_GAMES.append(game)

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