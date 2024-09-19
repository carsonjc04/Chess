class ChessGame:
    def __init__(self):
        # Initialize the board state
        self.board = self.create_board()
        self.turn = 'w'  # 'w' for white, 'b' for black

    def create_board(self):
        # Standard chess starting position
        return [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        ]

    def move_piece(self, start_pos, end_pos):
        """Moves a piece if the move is legal."""
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        piece = self.board[start_row][start_col]

        # Check if piece belongs to the current player
        if piece == "--" or piece[0] != self.turn:
            return False

        if self.is_valid_move(start_pos, end_pos, piece):
            self.board[end_row][end_col] = piece
            self.board[start_row][start_col] = "--"
            # Switch turn after a valid move
            self.turn = 'b' if self.turn == 'w' else 'w'
            return True
        return False

    def is_valid_move(self, start_pos, end_pos, piece):
        """Check if the move is valid based on the piece type."""
        piece_type = piece[1]
        if piece_type == 'P':  # Pawn
            return self.is_valid_pawn_move(start_pos, end_pos, piece)
        elif piece_type == 'R':  # Rook
            return self.is_valid_rook_move(start_pos, end_pos)
        elif piece_type == 'N':  # Knight
            return self.is_valid_knight_move(start_pos, end_pos)
        elif piece_type == 'B':  # Bishop
            return self.is_valid_bishop_move(start_pos, end_pos)
        elif piece_type == 'Q':  # Queen
            return self.is_valid_queen_move(start_pos, end_pos)
        elif piece_type == 'K':  # King
            return self.is_valid_king_move(start_pos, end_pos)
        return False

    def is_valid_pawn_move(self, start_pos, end_pos, piece):
        """Handle pawn movement."""
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        direction = -1 if piece[0] == 'w' else 1  # White moves up (-1), Black moves down (+1)

        # Regular forward move (no capture)
        if start_col == end_col:
            # One step forward
            if end_row == start_row + direction and self.board[end_row][end_col] == "--":
                return True
            # Two steps forward (only from the starting position)
            if (start_row == 6 and piece[0] == 'w') or (start_row == 1 and piece[0] == 'b'):
                if end_row == start_row + 2 * direction and self.board[end_row][end_col] == "--" and self.board[start_row + direction][start_col] == "--":
                    return True

        # Capture move (diagonal)
        if abs(start_col - end_col) == 1 and end_row == start_row + direction:
            if self.board[end_row][end_col] != "--" and self.board[end_row][end_col][0] != piece[0]:
                return True

        return False


    def is_valid_rook_move(self, start_pos, end_pos):
        """Handle rook movement."""
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        if start_row == end_row or start_col == end_col:
            return self.is_path_clear(start_pos, end_pos)
        return False

    def is_valid_knight_move(self, start_pos, end_pos):
        """Handle knight movement."""
        move_row = abs(end_pos[0] - start_pos[0])
        move_col = abs(end_pos[1] - start_pos[1])
        return (move_row == 2 and move_col == 1) or (move_row == 1 and move_col == 2)

    def is_valid_bishop_move(self, start_pos, end_pos):
        """Handle bishop movement."""
        if abs(start_pos[0] - end_pos[0]) == abs(start_pos[1] - end_pos[1]):
            return self.is_path_clear(start_pos, end_pos)
        return False

    def is_valid_queen_move(self, start_pos, end_pos):
        """Handle queen movement."""
        return self.is_valid_rook_move(start_pos, end_pos) or self.is_valid_bishop_move(start_pos, end_pos)

    def is_valid_king_move(self, start_pos, end_pos):
        """Handle king movement."""
        move_row = abs(end_pos[0] - start_pos[0])
        move_col = abs(end_pos[1] - start_pos[1])
        return move_row <= 1 and move_col <= 1

    def is_path_clear(self, start_pos, end_pos):
        """Check if the path between start and end is clear (for rooks, bishops, queens)."""
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        row_diff = end_row - start_row
        col_diff = end_col - start_col
        step_row = (row_diff // abs(row_diff)) if row_diff != 0 else 0
        step_col = (col_diff // abs(col_diff)) if col_diff != 0 else 0

        current_row, current_col = start_row + step_row, start_col + step_col
        while (current_row, current_col) != (end_row, end_col):
            if self.board[current_row][current_col] != "--":
                return False
            current_row += step_row
            current_col += step_col

        return True
