import pygame, sys, math
from pygame.locals import *
from pygame import gfxdraw
import time

class CLI:
    def __init__(self, board, logic_pfn):
        self.board = board
        self.logic = logic_pfn
        self.no_piece = '_'
        self.black_piece = '0'
        self.white_piece = '1'
        self.king_black = 'O'
        self.king_white = 'I'
    
    def show(self):
        print('\n\n\n')
        display_matrix = ''
        piece_ctr = 0
        for piece in self.board.get_board():
            if piece.player == None:
                display_matrix += f' {self.no_piece}'
            elif piece.player == 'white':
                if piece.king():
                    display_matrix += f' {self.king_white}'
                else:
                    display_matrix += f' {self.white_piece}'
            elif piece.player == 'black':
                if piece.king():
                    display_matrix += f' {self.king_black}'
                else:
                    display_matrix += f' {self.black_piece}'
            piece_ctr += 1
            if piece_ctr % 8 == 0:
                display_matrix += '\n'
        print(display_matrix)

    def get_move(self):
        timestamp_start = time.time() * 1000
        a = input('Select a move, format (x, y) (x, y). Ex: (1,2) (2,3)\n')
        
        try:
            moves = a.split(' ')
        except:
            print('Invalid move')
            return self.get_move()

        if not moves:
            print('Invalid move')
            return self.get_move()

        parsed_start, parsed_end = [x.replace(' ', '').replace('(', '').replace(')', '') for x in moves[0].split(',')], [x.replace(' ', '').replace('(', '').replace(')', '') for x in moves[1].split(',')]
        print(parsed_start, parsed_end)
        start, end = (int(parsed_start[0]), int(parsed_start[1])), (int(parsed_end[0]), int(parsed_end[1]))
        print(f'{start} {end}')

        piece = self.board.get_at(start)
        if self.board.get_at(end).get_player() == None and piece.get_player() == 'black':
            print(f'Moving black piece from {start} to {end}')
            move_type = self.logic.make_move(start, piece.get_player(), end)

            if move_type == 0:
                return timestamp_start

            total_jumps = self.logic.check_jumps(piece.get_key())
            if len(total_jumps) != 0:
                print('Total jumps len is {}'.format(len(total_jumps)))
                print(total_jumps)
                return (self.get_move(), timestamp_start)
    
    def game_loop(self):
        while True:
            self.show()
            ret = self.get_move()
            if isinstance(ret, tuple):
                ret = ret[1]
            timestamp_end = time.time() * 1000
            print(f'Player took turn lasting {int(timestamp_end - ret)} ms')
            self.logic.human_turn = not self.logic.human_turn
            self.logic.check_if_won('black')
            self.logic.ai_turn()
            self.logic.check_if_won('white')
            self.show()

class GameUI:
    def __init__(self, board, logic_pfn, size_x = 900, size_y = 900):
        self.board = board
        self.size_x = size_x
        self.size_y = size_y
        self.pieces_x = 8
        self.pieces_y = 8
        self.logic = logic_pfn
        self.sprite_rects = []
        self.state_wait_click = True

        pygame.init()
        self.display = pygame.display.set_mode((self.size_x, self.size_y), 0, 32)


    def draw_game(self):
        self.board = self.logic.get_board()
        self.sprite_rects = []
        self.piece_rects = {}
        self.display.fill((0, 0, 0))
        pygame.draw.rect(self.display, (146, 52, 0), (0, 0, self.size_x, self.size_y))
        
        white = True
        square_distance = int(self.size_y / 9)

        for y_offset in range(8):
            y_start = 50 + y_offset * square_distance
            x_start = 50

            for i in range(8):
                if white:
                    pygame.draw.rect(self.display, (240, 240, 240), (x_start + square_distance * i, y_start, square_distance, square_distance))
                else:
                    pygame.draw.rect(self.display, (34, 77, 34), (x_start + square_distance * i, y_start, square_distance, square_distance))
                white = not white
            white = not white

        for j in range(self.pieces_y):
            for i in range(self.pieces_x):
                if self.board.get_at((i, j)).get_player() == 'white':
                    if self.board.get_at((i, j)).king():
                        drawn_circle = pygame.draw.circle(self.display, (240, 240, 240), (100 + i * square_distance, 100 + j * square_distance), 39, 0)
                        pygame.gfxdraw.aacircle(self.display, 100 + i * square_distance, 100 + j * square_distance, 40, (240, 240, 240))
                        pygame.gfxdraw.filled_ellipse(self.display, 100 + i * square_distance, 100 + j * square_distance, 40, 40, (240, 240, 240))
                    else:
                        drawn_circle = pygame.draw.circle(self.display, (240, 240, 240), (100 + i * square_distance, 100 + j * square_distance), 24, 0)
                        pygame.gfxdraw.aacircle(self.display, 100 + i * square_distance, 100 + j * square_distance, 25, (240, 240, 240))
                        pygame.gfxdraw.filled_ellipse(self.display, 100 + i * square_distance, 100 + j * square_distance, 25, 25, (240, 240, 240))
                    self.piece_rects[self.board.get_at((i, j)).get_uuid()] = drawn_circle
                    self.sprite_rects += [drawn_circle]
                elif self.board.get_at((i, j)).get_player() == 'black':
                    if self.board.get_at((i, j)).king():
                        drawn_circle = pygame.draw.circle(self.display, (0, 0, 0), (100 + i * square_distance, 100 + j * square_distance), 39, 0)
                        pygame.gfxdraw.aacircle(self.display, 100 + i * square_distance, 100 + j * square_distance, 40, (0, 0, 0))
                        pygame.gfxdraw.filled_ellipse(self.display, 100 + i * square_distance, 100 + j * square_distance, 40, 40, (0, 0, 0))
                    else:
                        drawn_circle = pygame.draw.circle(self.display, (0, 0, 0), (100 + i * square_distance, 100 + j * square_distance), 24, 0)
                        pygame.gfxdraw.aacircle(self.display, 100 + i * square_distance, 100 + j * square_distance, 25, (0, 0, 0))
                        pygame.gfxdraw.filled_ellipse(self.display, 100 + i * square_distance, 100 + j * square_distance, 25, 25, (0, 0, 0))
                    self.piece_rects[self.board.get_at((i, j)).get_uuid()] = drawn_circle
                    self.sprite_rects += [drawn_circle]

    def render(self):
        sprite_in_question = None
        clock = pygame.time.Clock()
        timestamp_start, timestamp_end = time.time() * 1000, 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    if not self.logic.human_turn:
                        continue

                    pos = pygame.mouse.get_pos()
                    max_dist = 50

                    if sprite_in_question == None:
                        clicked_sprites = [min([(s, math.sqrt((pos[0] - s.x) * (pos[0] - s.x) + (pos[1] - s.y) * (pos[1] - s.y))) for s in self.sprite_rects], key=lambda x : x[1])]
                    
                        if clicked_sprites[0][1] >= max_dist:
                            print(f'Distance too large! {clicked_sprites[0][1]}')
                            continue

                        if len(clicked_sprites) != 1:
                            raise Exception(f"Error, expected len of 1, got {len(clicked_sprites)}")

                        sprite = clicked_sprites[0][0]
                        seeked_sprite = None

                        for k, v in self.piece_rects.items():
                            if v == sprite:
                                seeked_sprite = self.logic.get_piece_by_uuid(k)
                                break
                                
                        sprite_in_question = (sprite, seeked_sprite)
                        print(f'The sprite in question is {sprite_in_question}')

                    else:
                        p = (pos[0] - 50, pos[1] - 50)
                        if p[0] < 0 or p[1] < 0:
                            continue

                        if p[0] >= 800 or p[1] >= 800:
                            continue

                        x_pos = p[0] // 100
                        y_pos = p[1] // 100

                        drawn_sprite, piece = sprite_in_question
                        board_tmp = self.logic.get_board()

                        print(f'Tried to move from {piece.get_key()} to {(x_pos, y_pos)}')

                        if board_tmp.get_at((x_pos, y_pos)).get_player() == None:
                            move_type = self.logic.make_move(piece.get_key(), board_tmp.get_at(piece.get_key()).get_player(), (x_pos, y_pos))
                            self.logic.check_if_won('black')

                            if move_type == 1:
                                total_jumps = self.logic.check_jumps(piece.get_key())
                            
                                if len(total_jumps) != 0:
                                    sprite_in_question = None
                                    print('Total jumps len is {}'.format(len(total_jumps)))
                                    print(total_jumps)
                                    continue

                            timestamp_end = time.time() * 1000
                            print(f'Player took turn lasting {int(timestamp_end - timestamp_start)} ms')

                            self.logic.human_turn = not self.logic.human_turn
                            self.logic.ai_turn()
                            self.logic.check_if_won('white')
                            timestamp_start = time.time() * 1000
                        sprite_in_question = None


                elif event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            self.draw_game()
            pygame.display.update()
            clock.tick(60)