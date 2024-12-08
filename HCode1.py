import random

"""
This Class Generates a Sudoku Board with the following attributes:
  -row_length: The length of the grid (defaults to 9 for a 3 x 3 grid game)
  -removed_cells: Number of cells removed from game, defaults to 30 for easy difficulty
  -board: Represents the sudoku grid with a 2D List
  -box_length: The square root of row_length
"""

class SudokuGenerator:

  def __init__(self, row_length=9, removed_cells=30, board=None):  # initiates the class
      if board is None:
          board = []
      self.row_length = row_length
      self.removed_cells = removed_cells
      self.board = board
      for i in range(row_length):  # for loop establishes a row
          self.board.append([0] * row_length)  # then fills its columns with 0s [0, 0, 0, 0... 0] and goes to next row
      self.box_length = int(row_length ** 0.5)

  def check_board(self):  # checks if board is solved
      for row in range(9):
          for col in range(9):
              num = self.board[row][col]
              self.board[row][col] = 0  # temporarily sets that value to 0 to run is valid properly and not give us false valids
              if not self.is_valid(row, col, num):  # checks if valid, returning False if not
                  return False
              self.board[row][col] = num  # sets original value back to what it was
      return True

  def get_board(self):  # just returns the board
      return self.board

  def print_board(self):
      for row_index, row in enumerate(self.board):  # iterates through each board row
          if row_index % 3 == 0 and row_index != 0:  # if its the 3rd row value (4throw) split to make the 3 by 3 grid
              print("-----------------------")
          for col_index, num in enumerate(row):  # same thing but for columns
              if col_index % 3 == 0 and col_index != 0:
                  print(" | ", end="")
              if num == 0:
                  print(".", end=" ")
              else:
                  print(num, end=" ")
          print()  # goes to next line

  """
  Next 4 Methods:
  is_valid: Main method that checks number is valid to go on board. Uses 3 submethods to return True or False:
      -valid_in_row: checks if a number can be placed in a SINGULAR row, returns True if yes
      -valid_in_col: checks if a number can be placed in a SINGULAR column, returns True if yes
      -valid_in_box: checks if a number is not in a 3 x 3 subgrid box, returns True if yes
  """

  def valid_in_row(self, row, num):
      for col in range(self.row_length):  # checks every column in a row for same number.
          if self.board[row][col] == num:
              return False
      return True

  def valid_in_col(self, col, num):
      for row in range(self.row_length):  # checks every row in a column for same number.
          if self.board[row][col] == num:
              return False
      return True

  def valid_in_box(self, row_start, col_start, num):
      for row in range(row_start, row_start + 3):  # row tracker in 3 by 3 grid
          for col in range(col_start, col_start + 3):  # column tracker in 3 by 3 grid
              if self.board[row][
                  col] == num:  # comparis values in box row by row, iterating through all columns of row first from start points
                  return False
      return True

  def is_valid(self, row, col, num):
      return (
              self.valid_in_row(row, num)  # valid in row
              and self.valid_in_col(col, num)  # valid in column
              and self.valid_in_box(row - row % 3, col - col % 3, num)
      # valid in 3 x 3 square, parameters calculation ensures any point on grid is given a starting point for every individual 3x3 grid so function works
      )

  """
  Next 5 Methods:
      generate_sudoku: Outside of class but generates a sudoku board with a given difficulty. Has 3 submethods:
          -fill_diagonal: First step of generating Sudoku. Randomly fills the main diagonal of the board with numbers 1-9. Uses 1 Submethod:
              -fill_box: randomly fills in values in a 3 x 3 box
          -fill_remaining: Fills in the remaining cells of the board (provided by teacher, dont worry about it)
          -remove_cells: Once sudoku puzzle is generated, removes cells from board to create difficulty.
  """

  def fill_box(self, row_start, col_start):
      nums = list(range(1, self.row_length + 1))  # list of numbers 1 to 9
      random.shuffle(nums)  # shuffles the list of numbers
      for current_row in range(3):  # rows in 3 x 3 (range starts at 0)
          for current_col in range(3):  # columns in 3 x 3 (range starts at 0)
              self.board[row_start + current_row][
                  col_start + current_col] = nums.pop()  # last number in the list is removed and placed into specified empty space (pop works because it removes and returns last num)

  def fill_diagonal(self):
      for start_box_index in range(0, self.row_length, 3):  # starts at (0,0) to (3,3) to (6,6)
          self.fill_box(start_box_index, start_box_index)

  def fill_remaining(self, row, col):
      if (col >= self.row_length and row < self.row_length - 1):
          row += 1
          col = 0
      if row >= self.row_length and col >= self.row_length:
          return True
      if row < self.box_length:
          if col < self.box_length:
              col = self.box_length
      elif row < self.row_length - self.box_length:
          if col == int(row // self.box_length * self.box_length):
              col += self.box_length
      else:
          if col == self.row_length - self.box_length:
              row += 1
              col = 0
              if row >= self.row_length:
                  return True

      for num in range(1, self.row_length + 1):
          if self.is_valid(row, col, num):
              self.board[row][col] = num
              if self.fill_remaining(row, col + 1):
                  return True
              self.board[row][col] = 0
      return False

  def fill_values(self):  # provided by teacher, constructs a solution
      self.fill_diagonal()
      self.fill_remaining(0, self.box_length)

  def remove_cells(self):
      cells_removed = 0
      while cells_removed < self.removed_cells:  # while we have not removed the cells we need to remove
          row, col = random.randint(0, 8), random.randint(0, 8)  # choose random row and column
          if self.board[row][col] != 0:  # only remove cells that are not already empty
              self.board[row][col] = 0  # makes it empty
              cells_removed += 1

def generate_sudoku(size, removed):
  sudoku = SudokuGenerator(size, removed)
  sudoku.fill_values()
  sudoku.remove_cells()
  return sudoku.board

"""
Represents a single cell in the Sudoku board. 81 Cells are in one board
Attributes:
  value: the value of the cell (0 if empty)
  row: the row of the cell (0-8)
  col: the column of the cell (0-8)
  sketched_value: the value of the cell that exists (1-9) if exists, 0 if empty
  selected: True if the cell is selected, False if not
Methods explained in the code.
"""
class Cell:
  def __init__(self, value, row, col):  # Initializes Method
      self.value = value
      self.row = row
      self.col = col
      self.sketched_value = 0
      self.selected = False

  def set_cell_value(self, value):  # Sets the actual value of the cell (called when user inputs a number in the cell)
      self.value = value

  def set_sketched_value(self,
                         value):  # Keepts track of potential values of the cell / numbers typed but not submitted in it
      self.sketched_value = value

"""
A Class that represents an entire Sudoku Board.
Attributes:
  width, height: the width and height of the board
  screen: the pygame window that the board is on
  difficulty: the difficulty of the board
"""

class Board:
  def __init__(self, width, height, screen, difficulty):
      self.width = width
      self.height = height
      self.screen = screen
      self.difficulty = difficulty
      self.generator = SudokuGenerator(removed_cells=difficulty)
      self.board = generate_sudoku(width, difficulty)  # original board
      self.cells = []




      for row in range(9):  # populate the board with cell objects
          cell_row = []
          for col in range(9):
              cell_row.append(Cell(self.board[row][col], row, col))
          self.cells.append(cell_row)
      self.selected_cell = None  # no cell selected to start

  def select(self, row, col):
      if self.selected_cell:  # if a cell is already selected, deselect it
          self.selected_cell.selected = False
      self.selected_cell = self.cells[row][col]  # new cell
      self.selected_cell.selected = True

  def clear(self):  # will clear cell if selected and value is 0 (empty because not filled with permanent number)
      if self.selected_cell and self.selected_cell.value == 0:
          self.selected_cell.sketched_value = 0

  def place_number(self, value):
      if self.selected_cell and self.selected_cell.value == 0:  # if a cellis empty place number
          self.selected_cell.set_cell_value(value)

  def reset_to_original(self):
      for row in range(9):
          for col in range(9):
              if self.board[row][col] != 0:  # if cell is predifined do nothing
                  continue
              else:
                  self.cells[row][col].set_cell_value(0)  # turn it into 0
                  self.cells[row][col].set_sketched_value(0)

  def is_full(self):  # checks if a cell is full, returning false if 0 (empty)
      for row in self.cells:
          for cell in row:
              if cell.value == 0:
                  return False
      return True

  def update_board(self):  # gives specific cell a vale in the 2d list (nott the actual one)
      for row in range(9):
          for col in range(9):
              self.board[row][col] = self.cells[row][col].value

  def find_empty(self):  # same logic as check if full, but returns the first empty cell
      for row in range(9):
          for col in range(9):
              if self.cells[row][col].value == 0:
                  return row, col
      return None

  def check_board(self):  # checks if board is solved
      for row in range(9):
          for col in range(9):
              num = self.cells[row][col].value
              self.cells[row][
                  col].value = 0  # temporarily sets that value to 0 to run is valid properly and not give us false valids
              if not self.generator.is_valid(row, col, num):  # checks if valid, returning False if not
                  return False
              self.cells[row][col].value = num  # sets original valu back to what it was
      return True

sudoku = SudokuGenerator()
sudoku.board = [
  [5, 3, 0, 0, 7, 0, 0, 0, 0],
  [6, 0, 0, 1, 9, 5, 0, 0, 0],
  [0, 9, 8, 0, 0, 0, 0, 6, 0],
  [8, 0, 0, 0, 6, 0, 0, 0, 3],
  [4, 0, 0, 8, 0, 3, 0, 0, 1],
  [7, 0, 0, 0, 2, 0, 0, 0, 6],
  [0, 6, 0, 0, 0, 0, 2, 8, 0],
  [0, 0, 0, 4, 1, 9, 0, 0, 5],
  [0, 0, 0, 0, 8, 0, 0, 7, 9],
]
sudoku.print_board()
