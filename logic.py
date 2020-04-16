from gameui import GameUI
from board import Piece, Board
from ai import CheckersAI

class CheckersLogic:
    def __init__(self):
        self.board = Board(8, 8, options={None: 1, 'white': 1, 'black': 1})
        self.piece_map = {}
        self.piece_total = 0
        self.piece_ctr = 0
        self.human_turn = True
        self.tree_depth = 5
        self.ai = CheckersAI()

    def get_piece_by_uuid(self, uuidh):
        if uuidh not in self.piece_map:
            raise Exception(f'Did not find piece with uuid {uuidh} in piece map!')

        return self.piece_map[uuidh]
    
    def init_pieces(self):
        white = True
        for j in range(3):
            for i in range(8):
                if white:
                    self.board.set_at((i + (j + 1) % 2, j), 'white')
                else:
                    self.board.set_at((8 - i - (j + 1) % 2, 8 - j - 1), 'black')
                white = not white
                i += 1

        for j in range(8):
            for i in range(8):
                if self.board.get_at((i, j)) == None:
                    self.board.set_at((i, j), None)
                    continue
                if self.board.get_at((i, j)).get_player() == 'white' or self.board.get_at((i, j)).get_player() == 'black':
                    self.piece_map[self.board.get_at((i, j)).get_uuid()] = self.board.get_at((i, j))
                    self.piece_total += 1

        self.piece_ctr = self.piece_total

    def check_moves(self, key, absolute=False):
        is_king = True if self.board.get_at(key).king() else False
        is_white = True if self.board.get_at(key).get_player() == 'white' else False
        white_moves = [(-1, 1), (1, 1)]
        black_moves = [(-1, -1), (1, -1)]
        king_moves = white_moves + black_moves

        move_list = []
        move_set = king_moves if is_king else (white_moves if is_white else black_moves)
        
        for move in move_set:
                try:
                    if self.board.get_at((key[0] + move[0], key[1] + move[1])).get_player() == None:
                        if not absolute:
                            if (key[0] + move[0]) >= 0 and (key[1] + move[1]) >= 0 and (key[0] + move[0]) <= 7 and (key[1] + move[1]) <= 7:
                                move_list += [move]
                        else:
                            if (key[0] + move[0]) >= 0 and (key[1] + move[1]) >= 0 and (key[0] + move[0]) <= 7 and (key[1] + move[1]) <= 7:
                                move_list += [(key[0] + move[0], key[1] + move[1])]
                except:
                    pass

        return move_list

    def check_jumps(self, key, absolute=False):
        is_king = True if self.board.get_at(key).king() else False
        is_white = True if self.board.get_at(key).get_player() == 'white' else False
        white_jumps = [(-2, 2), (2, 2)]
        black_jumps = [(-2, -2), (2, -2)]
        king_jumps = white_jumps + black_jumps

        jump_list = []
        jump_set = king_jumps if is_king else (white_jumps if is_white else black_jumps)

        for jump in jump_set:
            try:
                if self.board.get_at((key[0] + jump[0] // 2, key[1] + jump[1] // 2)).get_player() == ('black' if is_white else 'white') and self.board.get_at((key[0] + jump[0], key[1] + jump[1])).get_player() == None:
                    if not absolute:
                        if (key[0] + jump[0]) >= 0 and (key[1] + jump[1]) >= 0 and (key[0] + jump[0]) <= 7 and (key[1] + jump[1]) <= 7:
                            jump_list += [jump]
                    else:
                        if (key[0] + jump[0]) >= 0 and (key[1] + jump[1]) >= 0 and (key[0] + jump[0]) <= 7 and (key[1] + jump[1]) <= 7:
                            jump_list += [(key[0] + jump[0], key[1] + jump[1])]
            except:
                pass

        return jump_list
    
    def check_if_won(self, player):
        opponent = 'white'
        if player == 'white':
            opponent = 'black'

        opponent_pieces = self.board.get_player_pieces(opponent)
        if len(opponent_pieces) == 0:
            return True

        total_moves, total_jumps = 0, 0

        for piece in opponent_pieces:
            tmp_moves = self.check_moves(piece)
            tmp_jumps = self.check_jumps(piece)

            total_moves += tmp_moves
            total_jumps += tmp_jumps

        if total_moves + total_jumps == 0:
            return True
        return False
    
    def make_move(self, key, player, to):
        player_moves = self.check_moves(key)
        player_jumps = self.check_jumps(key)

        dest = (to[0] - key[0], to[1] - key[1])
        if dest not in player_moves and dest not in player_jumps:
            raise Exception('Invalid move or jump!')

        if dest in player_moves:
            self.board.move_piece(key, to)
        else:
            self.board.move_piece(key, to)

    def ai_turn(self):
        value, origin, move = self.ai.minimax(self, 'white', self.tree_depth, [], 0)
        move = move[0]
        print(f'Computer moved with a cost of {value} [{origin}] -> [{move}]')
        self.human_turn = not self.human_turn
        self.make_move(origin, 'white', move)


    def get_board(self):
        return self.board

    def __getitem__(self, key):
        return self.board[key]

if __name__ == '__main__':
    logic = CheckersLogic()
    logic.init_pieces()
    game = GameUI(logic.get_board(), logic)
    game.render()