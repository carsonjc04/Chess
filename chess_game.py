import pygame
import sys
from chess_logic import ChessGame

# Initialize Pygame
pygame.init()

# Constants for board size and colors
WIDTH, HEIGHT = 800, 800
SQUARE_SIZE = WIDTH // 8
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")

# Load chess piece images
def load_images():
    pieces = ['bB', 'bK', 'bN', 'bP', 'bQ', 'bR', 'wB', 'wK', 'wN', 'wP', 'wQ', 'wR']
    images = {}
    for piece in pieces:
        images[piece] = pygame.transform.scale(pygame.image.load(f'images/{piece}.png'), (SQUARE_SIZE, SQUARE_SIZE))
    return images

# Draw the chessboard
def draw_board():
    screen.fill(WHITE)
    for row in range(8):
        for col in range(8):
            if (row + col) % 2 == 1:
                pygame.draw.rect(screen, BLACK, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Draw the pieces on the board
def draw_pieces(board, images):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != "--":
                screen.blit(images[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))

# Initialize game and images
game = ChessGame()
images = load_images()
selected_piece = None
start_pos = None

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            row, col = pygame.mouse.get_pos()[1] // SQUARE_SIZE, pygame.mouse.get_pos()[0] // SQUARE_SIZE
            if selected_piece:
                print(f"Attempting to move {selected_piece} from {start_pos} to {(row, col)}")
                if game.move_piece(start_pos, (row, col)):
                    print(f"Moved {selected_piece} to {(row, col)}")
                    selected_piece = None
                else:
                    print(f"Invalid move for {selected_piece}")
                    selected_piece = None
            else:
                # Selecting a piece to move
                selected_piece = game.board[row][col]
                if selected_piece != "--":
                    start_pos = (row, col)  # Set start position when a piece is selected
                    print(f"Selected piece: {selected_piece} at {start_pos}")

    # Redraw the board and pieces after every event
    draw_board()
    draw_pieces(game.board, images)
    pygame.display.update()
