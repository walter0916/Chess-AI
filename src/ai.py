from const import *
import copy

class AI:
  def __init__(self, color):
    self.color = color
    self.max_depth = 10  

  def make_move(self, board):
    best_move = self.find_best_move(board)
    return best_move

  def find_best_move(self, board):
    best_move = None
    best_score = float('-inf')

    # Iterate through all squares on the board
    for row in range(ROWS):
      for col in range(COLS):
        square = board.squares[row][col]

        # Check if the square has a piece belonging to the AI's color
        if square.has_piece() and square.piece.color == self.color:
          piece = square.piece

          # Calculate valid moves for the AI's piece
          board.calc_moves(piece, row, col, bool=True)

          # Iterate through valid moves for the piece
          for move in piece.moves:
          # Evaluate the move
            score = self.evaluate_move(board, piece, move)

            # Update best move if the current move has a higher score
            if score > best_score:
              best_score = score
              best_move = move

    return best_move

  def evaluate_move(self, board, piece, move):
    # Perform the move on a temporary board
    temp_board = copy.deepcopy(board)
    temp_board.move(piece, move, testing=True)

    # Get the value of the piece being moved
    piece_value = piece.value

    # Initialize the evaluation score
    evaluation_score = piece_value

    # Check if the move captures an opponent's piece
    if temp_board.squares[move.final.row][move.final.col].has_piece():
      captured_piece = temp_board.squares[move.final.row][move.final.col].piece
      evaluation_score += captured_piece.value  # Add the value of the captured piece

    # Check if the move puts the opponent's king in check
    if temp_board.in_check(piece, move):
      evaluation_score += 10  # Add a bonus for putting the opponent's king in check

    # Penalize moving pawns forward by only one square
    if piece.name == 'pawn':
      if move.initial.row == move.final.row - 1:  # If the pawn only moves one row forward
        evaluation_score -= 1  # Penalize moving pawns forward by only one square

    # Encourage advancing pieces towards the center of the board
    center_row, center_col = ROWS // 2, COLS // 2
    distance_to_center = abs(move.final.row - center_row) + abs(move.final.col - center_col)
    evaluation_score += 1 / (distance_to_center + 1)  # Encourage advancing towards the center

    # Encourage controlling the board by occupying more squares
    occupied_squares = sum(1 for row in temp_board.squares for square in row if square.has_piece())
    evaluation_score += occupied_squares / (ROWS * COLS)  # Encourage occupying more squares

    # Prioritize capturing opponent pieces if it doesn't put the AI's piece in danger
    if temp_board.squares[move.final.row][move.final.col].has_piece():
      if temp_board.squares[move.final.row][move.final.col].piece.color != piece.color:
        if not temp_board.in_check(temp_board.squares[move.final.row][move.final.col].piece, move):
          evaluation_score += captured_piece.value  # Add the value of the captured piece

    return evaluation_score

