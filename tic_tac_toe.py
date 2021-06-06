import pygame
from pygame.locals import *
import sys 

class Game:
    def __init__(self):
        self.board = Board()
        self.turn  = "O"
        self.status = 'PLAY'

    def show(self):
        self.board.show_game_board()

    def update_game(self, position):
        if self.status == 'GAME-OVER':
            return False

        if self.board.get_value(position) != 'E':
            return False
        
        self.board.update_board(position, self.turn)
        
        # check if end game
        if self.end_game(self.turn) == True:
            self.status = "GAME-OVER"
            self.board.show_game_board()
            return False
        
        # update game status 
        print ("Updated position: ", position)
        self.turn = 'X' if self.turn == 'O' else 'O'
        self.board.show_game_board()
    
    def end_game(self, turn):
        # horizontal
        board = self.get_board()
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] and board[i][0] != 'E':
                print ('Wygrane ', board[i][0])
                self.board.update_board([i, 0], 'R' + board[i][0])
                self.board.update_board([i, 1], 'R' + board[i][1])
                self.board.update_board([i, 2], 'R' + board[i][2])
                return True

        # vertical  
        for i in range(3):
            if board[0][i] == board[1][i] == board[2][i] and board[0][i] != 'E':
                print ('Wygrane ', board[0][i])
                self.board.update_board([0, i], 'R' + board[0][i])
                self.board.update_board([1, i], 'R' + board[1][i])
                self.board.update_board([2, i], 'R' + board[2][i])
                return True

        # cross-down
        if board[0][0] == board[1][1] == board[2][2] and board[0][0] != 'E':
            print ('Wygrane ', board[0][0])
            self.board.update_board([0, 0], 'R' + board[0][0])
            self.board.update_board([1, 1], 'R' + board[1][1])
            self.board.update_board([2, 2], 'R' + board[2][2])
            return True

        if board[0][2] == board[1][1] == board[2][0] and board[0][2] != 'E':
            print ('Wygrane ', board[0][2])
            self.board.update_board([0, 2], 'R' + board[0][2])
            self.board.update_board([1, 1], 'R' + board[1][1])
            self.board.update_board([2, 0], 'R' + board[2][0])
            return True

        return False

    def get_board(self):
        return self.board.get_board()

# "E" - Empty cell; "X" - Player X; "O" - Player O
class Board:
    def __init__(self):
        self.size = 3
        self.game_board = self.create_game_board()

    def create_game_board(self):
        self.game_board = list()
        for _ in range(self.size):
            temp_board = list()
            for _ in range(self.size):
                temp_board.append("E")
            self.game_board.append(temp_board)
        return self.game_board

    def update_board(self, position, turn):
        self.game_board[position[0]][position[1]] = turn

    def show_game_board(self):
        for i in range(self.size):
            for _ in range(self.size):
                print (self.game_board[i][_], end='\t')
            print ('')

    def get_value(self, position):
        return self.game_board[position[0]][position[1]] 

    def get_board(self):
        return self.game_board

class BoardObject:
    def __init__(self):
        pass 

# PYGAME ENGINE #
W, H = 720, 720
HW, HH = W/3, H/3

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
SOLID_FILL = 0

pygame.init()
DS = pygame.display.set_mode((W, H))
game = Game()
game.show()

def action_clicked_mouse(x, y):
    position = [int((y) / HH), int(x / HW)]
    game.update_game(position)

def events():
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit() 
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            action_clicked_mouse(x, y)

def draw(board):
    # Horizontal lines
    pygame.draw.line(DS, WHITE, (HW, 0), (HW, H), 5)
    pygame.draw.line(DS, WHITE, (HW*2, 0), (HW*2, H), 5)
    
    # Vertical lines
    pygame.draw.line(DS, WHITE, (0, HH), (W, HH), 5)
    pygame.draw.line(DS, WHITE, (0, HH*2), (W, HH*2), 5)

    for c in range(3):
        for r in range(3):
            if board[c][r] == 'O':
                pygame.draw.circle(DS, WHITE, (r*HW + HW/2, c*HH + HH/2), 100, 5)
            elif board[c][r] == 'X': 
                pygame.draw.line(DS, WHITE, (r*HW + 35, c*HH + 35), (r*HW + HW - 35, c*HH + HH - 35), 5)
                pygame.draw.line(DS, WHITE, (r*HW + 35, c*HH + HH - 35), (r*HW + HW - 35, c*HH + 35), 5)
            elif board[c][r] == 'RO':
                pygame.draw.circle(DS, RED, (r*HW + HW/2, c*HH + HH/2), 100, 5)
            elif board[c][r] == 'RX': 
                pygame.draw.line(DS, RED, (r*HW + 35, c*HH + 35), (r*HW + HW - 35, c*HH + HH - 35), 5)
                pygame.draw.line(DS, RED, (r*HW + 35, c*HH + HH - 35), (r*HW + HW - 35, c*HH + 35), 5)
                    

while True:
    events()
    draw(game.get_board())
    pygame.display.update()
    DS.fill(BLACK)
