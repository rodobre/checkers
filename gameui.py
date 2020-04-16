import pygame, sys
from pygame.locals import *
from pygame import gfxdraw

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
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    if not self.logic.human_turn:
                        continue

                    pos = pygame.mouse.get_pos()
                    clicked_sprites = [s for s in self.sprite_rects if s.collidepoint(pos)]

                    if sprite_in_question == None:
                        if len(clicked_sprites) != 1:
                            raise Exception(f"Error, expected len of 1, got {len(clicked_sprites)}")

                        sprite = clicked_sprites[0]
                        seeked_sprite = None

                        for k, v in self.piece_rects.items():
                            if v == sprite:
                                seeked_sprite = self.logic.get_piece_by_uuid(k)
                                break
                                
                        sprite_in_question = (sprite, seeked_sprite)
                        print(f'The sprite in question is {sprite_in_question}')
                    else:
                        if len(clicked_sprites) != 0:
                            continue

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
                            self.logic.make_move(piece.get_key(), board_tmp.get_at(piece.get_key()).get_player(), (x_pos, y_pos))

                        self.logic.human_turn = not self.logic.human_turn
                        self.logic.ai_turn()
                        sprite_in_question = None


                elif event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            self.draw_game()
            pygame.display.update()
            clock.tick(60)