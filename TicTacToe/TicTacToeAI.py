import tkinter as tk
from tkinter import messagebox

class TicTacToeGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("TIC TAC TOE — HUMAN VS AI")
        self.window.geometry("360x460")
        self.window.config(bg="#202020")
        self.window.resizable(False, False)
        self.current_player = "X"
        self.board = [None] * 9
        self.buttons = []
        title = tk.Label(self.window, text="TIC TAC TOE", font=("Arial", 28, "bold"), fg="white", bg="#202020")
        title.pack(pady=20)
        self.create_board()
        self.window.mainloop()
    def create_board(self):
        frame = tk.Frame(self.window, bg="#202020", bd=4, relief="ridge")
        frame.pack(pady=10)
        for i in range(9):
            btn = tk.Button(frame, text="", font=("Arial", 36, "bold"), width=3, height=1,
                            bg="#303030", fg="white", activebackground="#505050",
                            command=lambda i=i: self.handle_click(i))
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.buttons.append(btn)
    def handle_click(self, idx):
        if self.board[idx] is not None or self.current_player != "X":
            return
        self.make_move(idx, "X")
        if self.check_game_over():
            return
        self.window.after(300, self.ai_turn)
    def ai_turn(self):
        move = self.best_move()
        if move is not None:
            self.make_move(move, "O")
        self.check_game_over()
    def make_move(self, idx, player):
        self.board[idx] = player
        self.buttons[idx].config(text=player)
        self.current_player = "O" if player == "X" else "X"
    def best_move(self):
        best_score = -999
        move = None
        for i in range(9):
            if self.board[i] is None:
                self.board[i] = "O"
                score = self.minimax(False)
                self.board[i] = None
                if score > best_score:
                    best_score = score
                    move = i
        return move
    def minimax(self, is_max_turn):
        winner = self.check_winner()
        if winner == "O": return 10
        if winner == "X": return -10
        if all(self.board[i] is not None for i in range(9)): return 0
        if is_max_turn:
            best = -999
            for i in range(9):
                if self.board[i] is None:
                    self.board[i] = "O"
                    best = max(best, self.minimax(False))
                    self.board[i] = None
            return best
        else:
            best = 999
            for i in range(9):
                if self.board[i] is None:
                    self.board[i] = "X"
                    best = min(best, self.minimax(True))
                    self.board[i] = None
            return best
    def check_game_over(self):
        win = self.check_winner()
        if win:
            messagebox.showinfo("Game Over", win + " WINS!")
            self.reset_game()
            return True
        if all(self.board[i] is not None for i in range(9)):
            messagebox.showinfo("Game Over", "DRAW!")
            self.reset_game()
            return True
        return False
    def check_winner(self):
        lines = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        for a,b,c in lines:
            if self.board[a] and self.board[a] == self.board[b] == self.board[c]: return self.board[a]
        return None
    def reset_game(self):
        self.board = [None] * 9
        self.current_player = "X"
        for b in self.buttons: b.config(text="")

if __name__ == "__main__": TicTacToeGUI()