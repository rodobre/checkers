from copy import deepcopy
from math import inf

class CheckersAI:
    def get_score(self, piece_array):
        score = 0
        for piece in piece_array:
                if piece.king():
                        score += 150
                else:
                        score += 100
        return score
    
    def alpha_beta_pruning(self, clonelogic, player, depth, alpha = -inf, beta = inf, jump_path = []):
        logic = clonelogic

        white_pieces = logic.get_board().get_player_pieces('white')
        black_pieces = logic.get_board().get_player_pieces('black')

        if (player == 'white' and len(black_pieces) == 0) or (player == 'black' and len(white_pieces) == 0):
            print(f'Won game for player {player}')
            return (inf, None, None)
        elif (player == 'white' and len(white_pieces) == 0) or (player == 'black' and len(black_pieces) == 0):
            print(f'Lost game for player {player}')
            return (-inf, None, None)

        if depth == 0:
            return (self.get_score(white_pieces if player == 'white' else black_pieces) - self.get_score(black_pieces if player == 'white' else white_pieces), None, None)
        
        if jump_path:
            value = -inf if player == 'white' else inf

            if isinstance(jump_path[-1], list):
                jumps = logic.check_jumps(jump_path[-1][0], True)
            elif isinstance(jump_path[-1], tuple):
                jumps = logic.check_jumps(jump_path[-1], True)

            if jumps:
                best_jump = None
                for jump in jumps:
                    newlogic = deepcopy(logic)
                    newlogic.get_board().move_piece(jump_path[-1][0], jump)
                    is_king = newlogic.get_board().get_at(jump).king()

                    if is_king:
                        path_value = self.alpha_beta_pruning(newlogic, 'black' if player == 'white' else 'white', depth - 1, alpha, beta)[0]
                    else:
                        path_value = self.alpha_beta_pruning(newlogic, 'white' if player == 'white' else 'black', depth, alpha, beta, jump_path + [jump])[0]
                    
                    if player == 'white':
                        if path_value > value:
                            alpha = max(alpha, path_value)
                            value = path_value
                            best_jump = jump
                    else:
                        if path_value < value:
                            beta = min(beta, path_value)
                            value = path_value
                            best_jump = jump
                
                    if alpha >= beta:
                        break

                return (value, jump_path[-1], best_jump)
            else:
                return self.alpha_beta_pruning(logic, 'black' if player == 'white' else 'white', depth - 1, alpha, beta)
        else:
            value = -inf if player == 'white' else inf
            jumps = []

            for piece in white_pieces:
                piece_key = piece.get_key()
                jump_tmp = logic.check_jumps(piece_key, True)
                if jump_tmp:
                    jumps.append([jump_tmp, piece_key])

            if jumps:
                for jump, origin in jumps:
                    newlogic = deepcopy(logic)
                    newlogic.get_board().move_piece(origin, jump[0])
                    is_king = newlogic.get_board().get_at(jump[0]).king()
                    best_origin = None

                    if is_king:
                        path_value = self.alpha_beta_pruning(newlogic, 'black' if player == 'white' else 'white', depth - 1, alpha, beta)[0]
                    else:
                        path_value = self.alpha_beta_pruning(newlogic, 'white' if player == 'black' else 'black', depth, alpha, beta, jump_path + [jump])[0]
                    
                    if player == 'white':
                        if path_value > value:
                            alpha = max(alpha, path_value)
                            value = path_value
                            best_jump = jump
                            best_origin = origin
                    else:
                        if path_value < value:
                            beta = min(beta, path_value)
                            value = path_value
                            best_jump = jump
                            best_origin = origin

                    if alpha >= beta:
                        break
                
                return (value, best_origin, best_jump)
            else:
                value = -inf if player == 'white' else inf
                moves = []

                for piece in white_pieces:
                    piece_key = piece.get_key()
                    move_tmp = logic.check_moves(piece_key, True)
                    if move_tmp:
                        moves.append([move_tmp, piece_key])
                
                best_move, best_origin = None, None
                for move, origin in moves:
                    newlogic = deepcopy(logic)
                    newlogic.get_board().move_piece(origin, move[0])

                    path_value = self.alpha_beta_pruning(newlogic, 'black' if player == 'white' else 'white', depth - 1, alpha, beta)
                    path_value = path_value[0]

                    if player == 'white':
                        if path_value > value:
                            alpha = max(alpha, path_value)
                            value = path_value
                            best_move = move
                            best_origin = origin
                    else:
                        if path_value < value:
                            beta = min(beta, path_value)
                            value = path_value
                            best_move = move
                            best_origin = origin

                    if alpha >= beta:
                        break

                return (value, best_origin, best_move)

    def minimax(self, clonelogic, player, depth, jump_path = []):
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

            if isinstance(jump_path[-1], list):
                jumps = logic.check_jumps(jump_path[-1][0], True)
            elif isinstance(jump_path[-1], tuple):
                jumps = logic.check_jumps(jump_path[-1], True)

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
                piece_key = piece.get_key()
                jump_tmp = logic.check_jumps(piece_key, True)
                if jump_tmp:
                    jumps.append([jump_tmp, piece_key])

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
                    piece_key = piece.get_key()
                    move_tmp = logic.check_moves(piece_key, True)
                    if move_tmp:
                        moves.append([move_tmp, piece_key])
                
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
