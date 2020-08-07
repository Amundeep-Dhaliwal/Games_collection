import numpy, pygame, sys, time

board_rows = 6 # horizontal
board_cols = 7 # vertical

def create_board():
    board = numpy.zeros((board_rows,board_cols))
    return board

def drop_piece(board,row,col, piece):
    board[row][col] = piece 

def is_valid(board,col):
    return board[board_rows-1][col] == 0

def get_next_open_row(board, col):
    for r in range(board_rows):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(numpy.flip(board,0))

def winning_move(board, piece):
    for c in range(board_cols-3): # horizontal wins 
        for r in range(board_rows):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    for c in range(board_cols):
        for r in range(board_rows-3): # vertical wins
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    for c in range(board_cols-3): # positive slope diaganols
        for r in range(board_rows-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
    
    for c in range(board_cols-3): # positive slope diaganols
        for r in range(3,board_rows):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
    
def draw_board(board):
    for c in range(board_cols):
        for r in range(board_rows):
            pygame.draw.rect(screen, (0,0,255), (c*ss, r*ss+ss, ss, ss))
            pygame.draw.circle(screen, (0,0,0), (int(c*ss+ss/2), int(r*ss +ss+ ss/2)), radius)
    
    for c in range(board_cols):
        for r in range(board_rows):
            if board[r][c] ==1:
                pygame.draw.circle(screen, (255,0,0), (int(c*ss+ss/2), height - int(r*ss + ss/2)), radius)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, (255,255,0), (int(c*ss+ss/2), height - int(r*ss + ss/2)), radius)
    pygame.display.update()

def full_check(board):
    return not 0 in board 

board = create_board()
print_board(board)
game_over = False
turn = 1

pygame.init() # needs to be called to initialize pygame

ss = 100

width = board_cols * ss
height = (board_rows+1) * ss

size = (width, height)

radius = int(ss/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont('monospace', 75)

while not game_over:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, (0,0,0), (0,0,width, ss)) # blacks out all the previously drawn counters
            posx = event.pos[0]
            if turn == 1:
                pygame.draw.circle(screen, (255,0,0), (posx, int(ss/2)), radius)
            else:
                pygame.draw.circle(screen, (255,255,0), (posx, int(ss/2)), radius)
        pygame.display.update()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, (0,0,0), (0,0,width,ss))
            # Ask for player 1 input
            if turn ==1:
                posx = event.pos[0]
                col = posx//ss

                if is_valid(board, col):
                    row = get_next_open_row(board,col)
                    drop_piece(board, row, col, 1)

                    if winning_move(board, 1):
                        label = myfont.render('Player 1 wins!', 1, (255,0,0))
                        screen.blit(label, (40,10))
                        game_over = True
                        pygame.time.wait(100)
                
            else:
                posx = event.pos[0]
                col = posx//ss

                if is_valid(board, col):
                    row = get_next_open_row(board,col)
                    drop_piece(board, row, col, 2)

                    if winning_move(board, 2):
                        label = myfont.render('Player 2 wins!', 1, (255,255,0))
                        screen.blit(label, (40,10))
                        game_over = True
                        pygame.time.wait(100)
        
            if full_check(board):
                label = myfont.render('It\'s a tie!', 1, (255,255,255))
                screen.blit(label, (40,10))
                game_over = True
                pygame.time.wait(100)
            draw_board(board)
            turn *= -1 
time.sleep(2)