class Board:

    def __init__(self):
        """Initialize the board."""
        self.board = ["_" for _ in range(9)]
        self.winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8], # Columns
            [0, 4, 8], [2, 4, 6] # Diagonals
        ]
        self.winner = None
        self.game_over = False

    def print_board(self):
        """Print the board in a nice format where the index of the move is the position if the position is empty."""
        print("-------------")
        for i in range(3):
            #A is the index of the board position unless the position is empty in which case it value of the board at that index.
            a = i * 3 if self.board[i * 3] == "_" else self.board[i * 3]
            b = i * 3 + 1 if self.board[i * 3 + 1] == "_" else self.board[i * 3 + 1]
            c = i * 3 + 2 if self.board[i * 3 + 2] == "_" else self.board[i * 3 + 2]
            print("|", a, "|", b, "|", c, "|")
            print("-------------")

    def make_move(self, position, player):
        """
        Make a move on the board.

        :param position: The position to make the move.
        :param player: The player making the move.
        """
        if self.board[position] == "_":
            self.board[position] = player
            self.check_for_winner()
        else:
            raise Exception("Invalid move")
    
    def check_for_winner(self):
        """Check if there is a winner."""
        for combination in self.winning_combinations:
            if self.board[combination[0]] == self.board[combination[1]] == self.board[combination[2]] != "_":
                self.winner = self.board[combination[0]]
                self.game_over = True
                return
        if "_" not in self.board:
            self.game_over = True
            return
        self.game_over = False
    
    def get_valid_moves(self):
        """Get the valid moves."""
        return [i for i, x in enumerate(self.board) if x == "_"]
    
    def get_board_state(self):
        """Get the board state."""
        return "".join(self.board)
    
    def get_winner(self):
        """Get the winner."""
        return self.winner
    
    def is_game_over(self):
        """Check if the game is over."""
        return self.game_over
    
    def reset(self):
        """Reset the board."""
        self.board = ["_" for _ in range(9)]
        self.winner = None
        self.game_over = False