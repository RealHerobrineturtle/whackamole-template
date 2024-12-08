import pygame
import sys
from HCode1 import *

# Initialize PyGame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 700
GRID_SIZE = 540
CELL_SIZE = GRID_SIZE // 9
BUTTON_HEIGHT = 50
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Initialize Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Game")

# Fonts
FONT = pygame.font.Font(None, 36)

def draw_start_screen():
   screen.fill(WHITE)
   title = FONT.render("Sudoku Game", True, BLACK)
   screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))


   # Difficulty buttons
   easy_button = pygame.Rect(WIDTH // 4 - 50, 200, 100, 50)
   medium_button = pygame.Rect(WIDTH // 2 - 50, 200, 100, 50)
   hard_button = pygame.Rect(3 * WIDTH // 4 - 50, 200, 100, 50)


   pygame.draw.rect(screen, GRAY, easy_button)
   pygame.draw.rect(screen, GRAY, medium_button)
   pygame.draw.rect(screen, GRAY, hard_button)


   easy_text = FONT.render("Easy", True, BLACK)
   medium_text = FONT.render("Medium", True, BLACK)
   hard_text = FONT.render("Hard", True, BLACK)


   screen.blit(easy_text, (easy_button.x + (easy_button.width - easy_text.get_width()) // 2, easy_button.y + 10))
   screen.blit(medium_text,
               (medium_button.x + (medium_button.width - medium_text.get_width()) // 2, medium_button.y + 10))
   screen.blit(hard_text, (hard_button.x + (hard_button.width - hard_text.get_width()) // 2, hard_button.y + 10))


   pygame.display.flip()
   return easy_button, medium_button, hard_button




def draw_game_screen(board, selected_cell):
   screen.fill(WHITE)


   # Draw grid
   for i in range(10):
       line_width = 2 if i % 3 == 0 else 1
       pygame.draw.line(screen, BLACK, (CELL_SIZE * i, 0), (CELL_SIZE * i, GRID_SIZE), line_width)
       pygame.draw.line(screen, BLACK, (0, CELL_SIZE * i), (GRID_SIZE, CELL_SIZE * i), line_width)


   # Draw numbers and highlight selected cell
   for row in range(9):
       for col in range(9):
           if board[row][col] != 0:
               value = FONT.render(str(board[row][col]), True, BLACK)
               screen.blit(value, (col * CELL_SIZE + 20, row * CELL_SIZE + 20))
           if selected_cell == (row, col):
               pygame.draw.rect(screen, BLUE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)
               value = FONT.render(str(board[row][col]), True, RED)
               screen.blit(value, (col * CELL_SIZE + 20, row * CELL_SIZE + 20))

   # Draw buttons
   reset_button = pygame.Rect(50, GRID_SIZE + 10, 100, BUTTON_HEIGHT)
   restart_button = pygame.Rect(WIDTH // 2 - 50, GRID_SIZE + 10, 100, BUTTON_HEIGHT)
   exit_button = pygame.Rect(WIDTH - 150, GRID_SIZE + 10, 100, BUTTON_HEIGHT)


   pygame.draw.rect(screen, GRAY, reset_button)
   pygame.draw.rect(screen, GRAY, restart_button)
   pygame.draw.rect(screen, GRAY, exit_button)


   reset_text = FONT.render("Reset", True, BLACK)
   restart_text = FONT.render("Restart", True, BLACK)
   exit_text = FONT.render("Exit", True, BLACK)


   screen.blit(reset_text, (reset_button.x + 20, reset_button.y + 10))
   screen.blit(restart_text, (restart_button.x + 10, restart_button.y + 10))
   screen.blit(exit_text, (exit_button.x + 30, exit_button.y + 10))


   pygame.display.flip()
   return reset_button, restart_button, exit_button

def draw_end_screen(success):
   screen.fill(WHITE)
   message = "You Won!" if success else "Game Over!"
   message_text = FONT.render(message, True, BLUE if success else RED)
   screen.blit(message_text,
               (WIDTH // 2 - message_text.get_width() // 2, HEIGHT // 2 - message_text.get_height() // 2))
   if success:
       exit_button = pygame.Rect(WIDTH - 150, GRID_SIZE + 10, 100, BUTTON_HEIGHT)
       pygame.draw.rect(screen, GRAY, exit_button)
       exit_text = FONT.render("Exit", True, BLACK)
       screen.blit(exit_text, (exit_button.x + 50, exit_button.y + 10))
   else:
       restart_button = pygame.Rect(WIDTH // 2 - 50, GRID_SIZE + 10, 100, BUTTON_HEIGHT)
       pygame.draw.rect(screen, GRAY, restart_button)
       restart_text = FONT.render("Restart", True, BLACK)
       screen.blit(restart_text, (restart_button.x + 10, restart_button.y + 10))
   pygame.display.flip()

def get_cell_clicked(pos):
   if pos[0] < GRID_SIZE and pos[1] < GRID_SIZE:
       return pos[1] // CELL_SIZE, pos[0] // CELL_SIZE
   return None

def main():
   running = True
   selected_cell = None
   board = None
   easy_button, medium_button, hard_button = draw_start_screen()
   reset_button = restart_button = exit_button = None

   while running:
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               running = False
           elif event.type == pygame.MOUSEBUTTONDOWN:
               pos = pygame.mouse.get_pos()
               if not board:
                   # Handle difficulty selection
                   if easy_button.collidepoint(pos):
                       board = generate_sudoku(9, 30)
                       reset_button, restart_button, exit_button = draw_game_screen(board, selected_cell)


                   elif medium_button.collidepoint(pos):
                       board = generate_sudoku(9, 40)


                       reset_button, restart_button, exit_button = draw_game_screen(board, selected_cell)
                   elif hard_button.collidepoint(pos):
                       board = generate_sudoku(9, 50)
                       reset_button, restart_button, exit_button = draw_game_screen(board, selected_cell)


                   board_copy = [row[:] for row in board]
                   board_Boolean = [row[:] for row in board]
                   for x in range(9):
                       for y in range(9):
                           if board_Boolean[x][y] >=1:
                               board_Boolean[x][y] = True
                           else:
                               board_Boolean[x][y] = False
               else:
                   clicked_cell = get_cell_clicked(pos)
                   if clicked_cell:
                       selected_cell = clicked_cell
                       draw_game_screen(board, selected_cell)
                   elif reset_button.collidepoint(pos):
                       # Reset board
                       board = board_copy  # Adjust for initial board state
                       draw_game_screen(board_copy, selected_cell)
                   elif restart_button.collidepoint(pos):
                       board = None
                       easy_button, medium_button, hard_button = draw_start_screen()
                   elif exit_button.collidepoint(pos):
                       running = False
           elif event.type == pygame.KEYDOWN and selected_cell and board:
               row, col = selected_cell

               if event.key == pygame.K_RETURN:
                   generated = SudokuGenerator(9,30, board )
                   if generated.check_board():
                       draw_end_screen(True)
                       print("True")
                   else:
                       draw_end_screen(False)
                       print("False")
               elif pygame.K_1 <= event.key <= pygame.K_9 and not board_Boolean[row][col]:
                   value = event.key - pygame.K_0
                   board[row][col] = value
                   draw_game_screen(board, selected_cell)
               elif event.type == pygame.KEYDOWN and board:
                   if selected_cell:
                       row, col = selected_cell
                       if event.key == pygame.K_UP:
                           row = (row - 1) % 9
                       elif event.key == pygame.K_DOWN:
                           row = (row + 1) % 9
                       elif event.key == pygame.K_LEFT:
                           col = (col - 1) % 9
                       elif event.key == pygame.K_RIGHT:
                           col = (col + 1) % 9
                       selected_cell = (row, col)
                       draw_game_screen(board, selected_cell)

   pygame.quit()
   sys.exit()

if __name__ == "__main__":
   main()