from gameui import GameUI, CLI
from board import Piece, Board
from ai import CheckersAI
import sys
import time

class CheckersLogic:
    def __init__(self, tree_depth, algorithm):
        self.board = Board(8, 8, options={None: 1, 'white': 1, 'black': 1})
        self.piece_map = {}
        self.piece_total = 0
        self.piece_ctr = 0
        self.human_turn = True
        self.tree_depth = tree_depth
        self.algo_choice = 0 if algorithm == 'minimax' else 1
        self.timestamp_start = time.time() * 1000
        self.ai = CheckersAI()

    def print_time(self):
        timestamp_end = time.time() * 1000 - self.timestamp_start
        minu, seco = int(timestamp_end // 1000 // 60), int(timestamp_end // 1000 % 60)
        print('Game time -> {}:{}'.format('0' + str(minu) if minu <= 9 else str(minu), ('0' + str(seco) if seco <= 9 else str(seco))))

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
                if self.board.get_at((key[0] + jump[0] // 2, key[1] + jump[1] // 2)).get_player() == ('black' if is_white else 'white')  \
                    and self.board.get_at((key[0] + jump[0], key[1] + jump[1])).get_player() == None:
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
            print(f'[LOGIC] Player {player} has won the game, lack of opponent pieces')
            sys.exit(0)
            return True

        total_moves, total_jumps = 0,0

        for piece in opponent_pieces:
            tmp_moves = self.check_moves(piece.get_key())
            tmp_jumps = self.check_jumps(piece.get_key())

            if tmp_moves:
                total_moves += len(tmp_moves)
            if tmp_jumps:
                total_jumps += len(tmp_jumps)

        if total_moves + total_jumps == 0:
            print(f'[LOGIC] Player {player} has won the game, lack of opponent moves')
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
        
        if dest in player_moves:
            return 0
        elif dest in player_jumps:
            return 1
    
    def show_score(self, variant=0):
        black_pieces = self.board.get_player_pieces('black')
        white_pieces = self.board.get_player_pieces('white')

        if variant == 0:
            print(f'Black [{len(black_pieces)}] vs White [{len(white_pieces)}]')
        elif variant == 1:
            black_kings, white_kings = 0, 0
            for piece in black_pieces:
                if piece.king():
                    black_kings += 1
            for piece in white_pieces:
                if piece.king():
                    white_kings += 1
            print(f'Black [{(len(black_pieces) - black_kings) * 100 + black_kings * 150}] vs White [{(len(white_pieces) - white_kings) * 100 + white_kings * 150}]')
        
        self.print_time()
    
    def has_player_jumps(self, player):
        player_pieces = self.board.get_player_pieces(player)
        total_jumps = []
        for piece in player_pieces:
            tmp_jumps = self.check_jumps(piece.get_key())
            if tmp_jumps:
                total_jumps.append(tmp_jumps)
        if total_jumps:
            return True
        return False

    def ai_turn(self):
        timestamp_start = time.time() * 1000
        
        while True:
            if self.algo_choice == 0:
                ai_consideration = self.ai.minimax(self, 'white', self.tree_depth)
                value, origin, move = ai_consideration
            else:
                ai_consideration = self.ai.alpha_beta_pruning(self, 'white', self.tree_depth)
                value, origin, move = ai_consideration

            print(f'Computer moved with a cost of {value} [{origin}] -> [{move}]')
            self.make_move(origin, 'white', move)

            is_it_a_jump = True if ((abs(move[0] - origin[0]) + abs(move[1] - origin[1])) > 2) else False
            if not self.has_player_jumps('white') or not is_it_a_jump:
                break

        self.human_turn = not self.human_turn

        timestamp_finish = time.time() * 1000 - timestamp_start
        print(f'AI took a turn which lasted {int(timestamp_finish)} ms')
        self.show_score(0)
        self.show_score(1)


    def get_board(self):
        return self.board

    def __getitem__(self, key):
        return self.board[key]

if __name__ == '__main__':
    args = sys.argv
    if len(args) != 4:
        print('Invalid arguments')
        sys.exit(0)
    tree_depth = int(args[2])
    algorithm = args[3]

    if algorithm != 'minimax' and algorithm != 'abp':
        print('Algorithm must be either \"minimax\" or \"abp\" for ab pruning')
    
    logic = CheckersLogic(tree_depth, algorithm)
    logic.init_pieces()

    if args[1] == 'gui':
        game = GameUI(logic.get_board(), logic)
        game.render()
    elif args[1] == 'cli':
        game = CLI(logic.get_board(), logic)
        game.game_loop()
