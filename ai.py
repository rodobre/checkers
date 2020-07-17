from copy import deepcopy
from math import inf
import sys

class CheckersAI:
    def get_score(self, piece_array):
        score = 0
        for piece in piece_array:
            if piece.king():
                score += 150
            else:
                score += 100
        return score

    # 0 if jump, 1 if move
    def get_player_actions(self, player, logic, move=0, pieces=None):
        board = logic.get_board()
        total_actions = []

        if pieces == None:
            pieces = board.get_player_pieces(player)

        for piece in pieces:
            piece_key = piece.get_key()
            tmp_action = logic.check_jumps(piece_key, True) if move == 0 else logic.check_moves(piece_key, True)

            if tmp_action:
                for mv in tmp_action:
                    total_actions.append((mv, piece_key))

        return total_actions

    def get_best_continuation_jump(self, player, player_pieces, logic, board, depth, algo, origin, alpha = -inf, beta = inf):
        if not origin:
            return None
        
        opponent_player = 'black' if player == 'white' else 'white'
        value = -inf if player == 'white' else inf
        last_jump = origin[-1]
        jumps = logic.check_jumps(last_jump, True)

        if jumps:
            best_jump = None
            new_logic = None
            for jump in jumps:
                new_logic = deepcopy(logic)
                new_logic.get_board().move_piece(last_jump, jump)
                is_king = new_logic.get_board().get_at(jump).king()

                if is_king:
                    if algo == self.minimax:
                        path_value = algo(new_logic, opponent_player, depth - 1)[0]
                    else:
                        path_value = algo(new_logic, opponent_player, depth - 1, [], -inf, inf)[0]
                else:
                    if algo == self.minimax:
                        path_value = algo(new_logic, player, depth, origin + [jump])[0]
                    else:
                        path_value = algo(new_logic, player, depth, origin + [jump], -inf, inf)[0]
                
                if ((path_value > value) if player == 'white' else (path_value < value)):
                    alpha = max(alpha, path_value) if player == 'white' else alpha
                    beta = min(beta, path_value) if player == 'black' else beta
                    value = path_value
                    best_jump = jump
                
                if alpha >= beta:
                    break

            return (value, last_jump, best_jump)
        else:
            return algo(logic, opponent_player, depth - 1)


    def get_best_action(self, player, player_pieces, logic, board, depth, algo, action_type, alpha = -inf, beta = inf):
        player_actions = self.get_player_actions(player, logic, action_type, player_pieces)

        if not player_actions:
            return None
        
        opponent_player = 'black' if player == 'white' else 'white'
        value = -inf if player == 'white' else inf
        best_action = None
        best_origin = None

        for action, action_origin in player_actions:
            new_logic = deepcopy(logic)
            new_logic.get_board().move_piece(action_origin, action)
            is_king = new_logic.get_board().get_at(action).king()

            if is_king:
                if algo == self.minimax:
                    path_value = algo(new_logic, opponent_player, depth - 1)[0]
                else:
                    path_value = algo(new_logic, opponent_player, depth - 1, [], alpha, beta)[0]
            else:
                if algo == self.minimax:
                    path_value = algo(new_logic, player, depth, [action])[0]
                else:
                    path_value = algo(new_logic, player, depth, [action], alpha, beta)[0]
                        
            if ((path_value > value) if player == 'white' else (path_value < value)):
                alpha = max(alpha, path_value) if player == 'white' else alpha
                beta = min(beta, path_value) if player == 'black' else beta
                value = path_value
                best_action = action
                best_origin = action_origin

            if (alpha >= beta):
                break

        return (value, best_origin, best_action)

    def alpha_beta_pruning(self, clonelogic, player, depth, jump_path = [], alpha = -inf, beta = inf):
        return self.minimax(clonelogic, player, depth, jump_path, alpha, beta, True)

    def minimax(self, clonelogic, player, depth, jump_path = [], alpha = -inf, beta = inf, is_this_abp = False):
        logic = clonelogic
        board = logic.get_board()

        player_pieces = board.get_player_pieces(player)
        opponent_pieces = board.get_player_pieces('white') if player == 'black' else board.get_player_pieces('black')
        is_player_white = (player == 'white')
        white_pieces = player_pieces if is_player_white else opponent_pieces
        black_pieces = opponent_pieces if is_player_white else player_pieces

        # clear win for player, return state
        if not player_pieces and is_player_white:
            return (-inf, None, None)
        elif not player_pieces and not is_player_white:
            return (inf, None, None)
        
        # clear win for opponent, return state
        if not opponent_pieces and is_player_white:
            return (inf, None, None)
        elif not opponent_pieces and not is_player_white:
            return (-inf, None, None)
        
        # end of recursion tree, return score
        if depth == 0:
            return (self.get_score(white_pieces) - self.get_score(black_pieces), None, None)

        # follow jump path
        if jump_path:
            if is_this_abp:
                next_jump = self.get_best_continuation_jump(player, player_pieces, logic, board, depth, self.alpha_beta_pruning, jump_path, alpha, beta)
            else:
                next_jump = self.get_best_continuation_jump(player, player_pieces, logic, board, depth, self.minimax, jump_path)

            if next_jump == None:
                raise Exception('None here?')
            
            return next_jump
        else:

            if is_this_abp:
                jumps = self.get_best_action(player, player_pieces, logic, board, depth, self.alpha_beta_pruning, 0, alpha, beta)
            else:
                jumps = self.get_best_action(player, player_pieces, logic, board, depth, self.minimax, 0)

            if jumps:
                    return jumps

            if is_this_abp:
                moves = self.get_best_action(player, player_pieces, logic, board, depth, self.alpha_beta_pruning, 1, alpha, beta)
            else:
                moves = self.get_best_action(player, player_pieces, logic, board, depth, self.minimax, 1)

            if moves:
                return moves
        
        # no moves or jumps to be made, what do we do ? stalemate
        return (-inf, None, None)