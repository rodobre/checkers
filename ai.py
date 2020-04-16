from copy import deepcopy
from math import inf

class CheckersAI:
    def get_score(self, piece_array):
        score = 0
        for piece in piece_array:
            if piece.king():
                score += 3
            else:
                score += 1
        return score

    def minimax(self, clonelogic, player, depth, jump_path = [], muie = 0):
        logic = clonelogic

        white_pieces = logic.get_board().get_player_pieces('white')
        black_pieces = logic.get_board().get_player_pieces('black')

        if len(white_pieces) == 0:
            return (-inf, None, None)
        
        if len(black_pieces) == 0:
            return (inf, None, None)

        if depth == 0:
            return (self.get_score(white_pieces if player == 'white' else black_pieces) - self.get_score(black_pieces if player == 'white' else white_pieces), None, None)
        
        if jump_path:
            value = -inf if player == 'white' else inf
            jumps = logic.check_jumps(jump_path[-1][0], True)

            if jumps:
                best_jump = None
                for jump in jumps:
                    newlogic = deepcopy(logic)
                    newlogic.get_board().move_piece(jump_path[-1][0], jump)
                    is_king = newlogic.get_board().get_at(jump).king()

                    if is_king:
                        path_value = self.minimax(newlogic, 'black' if player == 'white' else 'white', depth - 1)[0]
                    else:
                        path_value = self.minimax(newlogic, 'white' if player == 'white' else 'black', depth, jump_path + [jump])[0]
                    
                    if player == 'white':
                        if path_value > value:
                            value = path_value
                            best_jump = jump
                    else:
                        if path_value < value:
                            value = path_value
                            best_jump = jump
                
                return (value, jump_path[-1], best_jump)
            else:
                return self.minimax(logic, 'black' if player == 'white' else 'white', depth - 1)
        else:
            value = -inf if player == 'white' else inf
            jumps = []
            for piece in white_pieces:
                jump_tmp = logic.check_jumps(piece.get_key(), True)
                if jump_tmp:
                    jumps.append([jump_tmp, piece.get_key()])

            if jumps:
                for jump, origin in jumps:
                    newlogic = deepcopy(logic)
                    newlogic.get_board().move_piece(origin, jump[0])
                    is_king = newlogic.get_board().get_at(jump[0]).king()

                    if is_king:
                        path_value = self.minimax(newlogic, 'black' if player == 'white' else 'white', depth - 1)[0]
                    else:
                        path_value = self.minimax(newlogic, 'white' if player == 'black' else 'black', depth, jump_path + [jump])[0]
                    
                    if player == 'white':
                        if path_value > value:
                            value = path_value
                            best_jump = jump
                            best_origin = origin
                    else:
                        if path_value < value:
                            value = path_value
                            best_jump = jump
                            best_origin = origin

                return (value, best_origin, best_jump)
            else:
                value = -inf if player == 'white' else inf
                moves = []
                for piece in white_pieces:
                    move_tmp = logic.check_moves(piece.get_key(), True)
                    if move_tmp:
                        moves.append([move_tmp, piece.get_key()])
                
                best_move, best_origin = None, None
                for move, origin in moves:
                    newlogic = deepcopy(logic)
                    newlogic.get_board().move_piece(origin, move[0])

                    path_value = self.minimax(newlogic, 'black' if player == 'white' else 'white', depth - 1)
                    path_value = path_value[0]

                    if player == 'white':
                        if path_value > value:
                            value = path_value
                            best_move = move
                            best_origin = origin
                    else:
                        if path_value < value:
                            value = path_value
                            best_move = move
                            best_origin = origin
                
                return (value, best_origin, best_move)