import tkinter


class GameLogic(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("XO-Battle")
        self.geometry("700x600")
        self.config(padx=10, pady=10)
        self.current_player = ""
        self.grid = []
        self.x_score = 0
        self.o_score = 0
        # self.game_over = False

    def player_turn(self):
        if self.current_player == "X":
            self.current_player = "O"
        else:
            self.current_player = "X"
        turn_text = tkinter.Label(
            self, text=f"Player {self.current_player}'s turn")
        turn_text.grid(row=1, column=0, columnspan=3,
                       sticky="ew", pady=(10, 20))

    def start_game(self):
        for row in range(3):
            for column in range(3):
                current_row = row
                current_column = column
                self.grid[row][column].config(
                    command=lambda r=current_row, c=current_column: self.handle_click(r, c))

    def handle_click(self, row, column):
        # Detect if the button is clicked, and update button text with current player
        if self.grid[row][column]["text"] == "":
            self.grid[row][column]["text"] = self.current_player
            winner = self.check_winner()
            if winner:
                self.update_score()
                self.show_game_over_message()
                self.reset_game()
            elif self.is_grid_full():
                self.show_game_over_message()
                self.reset_game()
            else:
                self.player_turn()

    def check_winner(self):
        # Check horizontal rows
        for row in range(3):
            if self.grid[row][0]["text"] == self.grid[row][1]["text"] == self.grid[row][2]["text"] != "":
                return self.grid[row][0]["text"]

        # Check vertical columns
        for col in range(3):
            if self.grid[0][col]["text"] == self.grid[1][col]["text"] == self.grid[2][col]["text"] != "":
                return self.grid[0][col]["text"]

        # Check diagonals
        if self.grid[0][0]["text"] == self.grid[1][1]["text"] == self.grid[2][2]["text"] != "":
            return self.grid[0][0]["text"]
        if self.grid[0][2]["text"] == self.grid[1][1]["text"] == self.grid[2][0]["text"] != "":
            return self.grid[0][2]["text"]

        # Check for draw
        if self.is_grid_full():
            return "Draw"

        return None

    def update_score(self):
        winner = self.check_winner()
        if winner == "X":
            self.x_score += 1
        elif winner == "O":
            self.o_score += 1
        self.update_score_board()

    def update_score_board(self):
        score_board = tkinter.Label(
            self, text=f"X: {self.x_score} | O: {self.o_score}", font=("Arial", 16))
        score_board.grid(row=0, column=0, columnspan=3,
                         sticky="ew", pady=(10, 20))

    def reset_game(self):
        self.remove_game_over_message()  # Remove any existing game over message
        for row in range(3):
            for column in range(3):
                self.grid[row][column]["text"] = ""
        self.current_player = ""
        self.player_turn()

    def is_grid_full(self):
        return all(self.grid[i][j]["text"] != "" for i in range(3) for j in range(3))

    def show_game_over_message(self):
        winner = self.check_winner()
        if winner == "Draw":
            message = "Game Over! It's a Draw!"
        else:
            message = f"Game Over! Player {winner} wins!"
        self.game_over_label = tkinter.Label(
            self, text=message, font=("Arial", 16))
        self.game_over_label.grid(row=4, column=0, columnspan=3, pady=20)
        # Schedule the message to be removed after 2 seconds
        self.after(2000, self.remove_game_over_message)

    def remove_game_over_message(self):
        self.game_over_label.config(text="")
