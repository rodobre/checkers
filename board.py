import uuid

class Piece:
    def __init__(self, key, player):
        if not isinstance(key, tuple):
            raise Exception('Received wrong key for piece, expected \'tuple\', got {}'.format(type(key)))

        if len(key) != 2:
            raise Exception('Coordinate tuple of invalid length in piece constructor, expected 2, got {}'.format(len(key)))

        self.player = player
        self.x = key[0]
        self.y = key[1]
        self.is_king = False
        self.uuid = str(uuid.uuid4())

    def get_uuid(self):
        return self.uuid

    def get_player(self):
        return self.player

    def get_key(self):
        return (self.x, self.y)

    def set_key(self, key):
        self.x, self.y = key
        if self.y == 0:
            if self.player == 'black':
                self.set_king()
        elif self.y == 7:
            if self.player == 'white':
                self.set_king()

    def king(self):
        return self.is_king
    
    def set_king(self):
        self.is_king = True

    def __repr__(self):
        return f'Piece(uuid={self.uuid}, x={self.x}, y={self.y}, player={str(self.player)})'

class Board:
    # da, options este un hash table, nu un array
    # da, imi place sa o ard O(1)
    # mai zi ceva
    def __init__(self, size_x, size_y, options = {None: 1, '0': 1, '1': 1}):
        self.board_size_x = size_x
        self.board_size_y = size_y
        self.board = [None] * self.board_size_x * self.board_size_y
        self.options = options
        self.player_pieces = {}
    
    def get_board_size(self):
        return (self.board_size_x, self.board_size_y)
    
    def get_board(self):
        return self.board
    
    def get_at_idx(self, idx):
        if idx < 0 or idx >= len(self.board):
            raise Exception('Board idx is not within the range. Got \'{}\' larger than \'{}\''.format(idx, len(self.board)))
        return self.board[idx]

    def get_at(self, key):
        if not isinstance(key, tuple):
            raise Exception('Board key is not a tuple! Got \'{}\' instead.'.format(type(key)))

        if len(key) != 2:
            raise Exception('Board key does not represent a coordinate! Size: {}'.format(len(key)))

        x, y = key
        if x >= self.board_size_x:
            raise Exception('Board key has abscissa larger than board size! X: {} Board size X: {}'.format(x, self.board_size_x))

        if y >= self.board_size_y:
            raise Exception('Board key has ordonate larger than board size! Y: {} Board size Y: {}'.format(y, self.board_size_y))

        return self.board[y * self.board_size_y + x]


    def set_at(self, key, piece):
        if piece not in self.options:
            raise Exception('Option is not in board options! Got \'{}\''.format(piece))

        if not isinstance(key, tuple):
            raise Exception('Board key is not a tuple! Got \'{}\' instead.'.format(type(key)))

        if len(key) != 2:
            raise Exception('Board key does not represent a coordinate! Size: {}'.format(len(key)))

        x, y = key
        if x >= self.board_size_x:
            raise Exception('Board key has abscissa larger than board size! X: {} Board size X: {}'.format(x, self.board_size_x))

        if y >= self.board_size_y:
            raise Exception('Board key has ordonate larger than board size! Y: {} Board size Y: {}'.format(y, self.board_size_y))

        self.board[y * self.board_size_y + x] = Piece(key, piece)
    
    def get_player_pieces(self, player):
        pieces = []
        for piece in self.board:
            if piece.get_player() == player:
                pieces.append(piece)
        return pieces

    def move_piece(self, pos, goto_pos):
        diff = abs(goto_pos[1] - pos[1]) + abs(goto_pos[0] - pos[0])
        if diff > 2:
            # skip, not move
            middle = ((goto_pos[0] + pos[0]) // 2, (goto_pos[1] + pos[1]) // 2)
            self.set_at(middle, None)

        self.board[pos[1] * self.board_size_y + pos[0]].set_key(goto_pos)
        self.board[goto_pos[1] * self.board_size_y + goto_pos[0]].set_key(pos)
        i, j = self.board[pos[1] * self.board_size_y + pos[0]], self.board[goto_pos[1] * self.board_size_y + goto_pos[0]]
        self.board[pos[1] * self.board_size_y + pos[0]], self.board[goto_pos[1] * self.board_size_y + goto_pos[0]] = j, i
    
    def __getitem__(self, key):
        return self.get_at(key)

    def __repr__(self):
        ret = ''
        for p in self.board:
            ret += repr(p) + ', '
        return ret