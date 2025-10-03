import tkinter as tk

class Game:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Cat Game")

        self.board = [None] * 16 # 4x4 
        self.buttons = []

        # Initialize logic
        self.ai = Initial(self.board) # Call the other class to sustract their functions

        self.create_board() # Call the function to create the board
        self.root.mainloop() # Call main to run all the program

    def create_board(self):
        for i in range(16):
            btn = tk.Button(self.root, text="", font=("Arial", 20), width=7, height=3,
                            command=lambda i=i: self.player_move(i))
            btn.grid(row=i // 4, column=i % 4)
            self.buttons.append(btn)

    def player_move(self, index):
        if self.board[index] is None:
            self.board[index] = "O"
            self.buttons[index].config(text="O", state="disabled")

            if self.ai.evaluate(self.board, 0) == -1000:  # jugador gana
                self.end_game("You won!")
                return

            if self.ai.is_full(self.board):
                self.end_game("Game tie")
                return

            # AI
            self.ai_move()

    def ai_move(self):
        best_score = -float("inf")
        best_move = None

        for move in self.ai.get_moves(self.board):
            new_board = self.ai.make_move(self.board, move, "X")
            score = self.ai.minimax(new_board, depth=6, alpha=-float("inf"), beta=float("inf"), is_max=False)
            if score > best_score:
                best_score = score
                best_move = move

        if best_move is not None:
            self.board[best_move] = "X"
            self.buttons[best_move].config(text="X", state="disabled")

        if self.ai.evaluate(self.board, 0) == 1000:
            self.end_game("The computer won!")
        elif self.ai.is_full(self.board):
            self.end_game("Game tie")

    def end_game(self, message):
        for btn in self.buttons:
            btn.config(state="disabled")
        result = tk.Label(self.root, text=message, font=("Arial", 16))
        result.grid(row=5, column=0, columnspan=4)

class Initial():

    def __init__(self, board):
        self.board = board

    def evaluate(self, board, depth):
        win_contion = [(0, 1, 2, 3), (4, 5, 6, 7), (8, 9, 10, 11), (12, 13, 14, 15), # row horizontal
                       (0, 5, 10, 15), (3, 6, 9, 12), # diagonal
                       (0, 4, 8, 12), (1, 5, 9, 13), (2, 6, 10, 14), (3, 7, 11, 15) # columns vertical
                      ]
        for index in win_contion:
            p1, p2, p3, p4 = index # 4 items (p1, p2, p3, p4) index that is validate with Xs or Os
            # Victory condition
            if board[p1] == board[p2] == board[p3] == board[p4] and board[p1] != None: # if all the indexs are equal and is not none 
                if board[p1] == 'X':
                    return 1000 + depth# MAX (AI) WIN
                else: return -1000 + depth# MIN (PLAYER) WIN
        return 0
        
     # If none is in board, we have spaces without value, so, the board is not full
    def is_full(self, board):
        return all(cell is not None for cell in board)

    def get_moves(self, board):
        moves = [] # To save the moves
        for position in range(len(board)): 
            if board[position] is None: # If each position inside board is None (the cell do not have value) 
                moves.append(position) # insert data
        return moves
    
    def make_move(self, board, move, player):
        new_board = board.copy() # With function .copy() literally copy the list of board 
        new_board[move] = player # to add moves ('X' OR 'O')  depend of the type of player
        return new_board
    
    def minimax(self, board, depth, alpha, beta, is_max):
        score = self.evaluate(board, depth) # evaluate if the game is finished and who won
        if score != 0 or depth == 0: # if the score is different 0 or depth is 0, the game is over
            return score
    
        if self.is_full(board):
            return 0 # We do not have winner -> Game tie
        
        # Player MAX (to maximize all) -> AI
        if is_max:
            max_eval = -float('inf') # Infinite number to max
            # iterate inside of function get_moves() to insert data when the position is None
            for move in self.get_moves(board): 
                new_board = self.make_move(board, move, "X") # 
                eval = self.minimax(new_board, depth - 1, alpha, beta, False) # recursion to 
                max_eval = max(max_eval, eval) # max between alpha and eval to get the max number
                alpha = max(alpha, eval)
                if beta <= alpha: # pruning
                    break
            return max_eval
        else: # Player MIN (to minimize all) -> Human
            min_eval = float('inf')
            for move in self.get_moves(board):
                new_board = self.make_move(board, move, "O")
                eval = self.minimax(new_board, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval


if __name__ == "__main__":
    Game()
