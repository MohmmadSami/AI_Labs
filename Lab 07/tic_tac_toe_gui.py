"""
====================================================
  LAB 06 - Tic Tac Toe Simple GUI
  Subject : Artificial Intelligence
  Library : tkinter (built-in — no install needed)
  Run     : python3 tic_tac_toe_gui.py
====================================================
"""

import math
import tkinter as tk
from tkinter import messagebox

# ── Theme ────────────────────────────────────────
BG      = "#f0f0f0"   # Window background
X_CLR   = "#e74c3c"   # Red  — AI (X)
O_CLR   = "#2980b9"   # Blue — Human (O)
BTN_BG  = "#ffffff"   # Empty cell color

# ── Evaluation Function ──────────────────────────
# Returns +10 (X wins), -10 (O wins), or 0
def evaluate(b):
    lines = [
        [b[0][0], b[0][1], b[0][2]],  # Row 0
        [b[1][0], b[1][1], b[1][2]],  # Row 1
        [b[2][0], b[2][1], b[2][2]],  # Row 2
        [b[0][0], b[1][0], b[2][0]],  # Col 0
        [b[0][1], b[1][1], b[2][1]],  # Col 1
        [b[0][2], b[1][2], b[2][2]],  # Col 2
        [b[0][0], b[1][1], b[2][2]],  # Diagonal
        [b[0][2], b[1][1], b[2][0]],  # Anti-diagonal
    ]
    for line in lines:
        if line[0] == line[1] == line[2] != '_':
            return 10 if line[0] == 'x' else -10
    return 0

def moves_left(b):
    # True if any empty cell exists
    return any(b[r][c] == '_' for r in range(3) for c in range(3))

# ── Minimax Algorithm ────────────────────────────
# AI (X) maximizes, Human (O) minimizes the score
def minimax(b, depth, is_max):
    score = evaluate(b)
    if score == 10:  return score - depth   # X wins
    if score == -10: return score + depth   # O wins
    if not moves_left(b): return 0          # Draw

    best = -math.inf if is_max else math.inf
    for r in range(3):
        for c in range(3):
            if b[r][c] == '_':
                b[r][c] = 'x' if is_max else 'o'   # Try move
                val  = minimax(b, depth + 1, not is_max)
                b[r][c] = '_'                       # Undo move
                best = max(best, val) if is_max else min(best, val)
    return best

# ── Find Best Move for AI ────────────────────────
def best_move(b):
    best_sc, move = -math.inf, (-1, -1)
    for r in range(3):
        for c in range(3):
            if b[r][c] == '_':
                b[r][c] = 'x'
                sc = minimax(b, 0, False)   # Score this move
                b[r][c] = '_'              # Undo
                if sc > best_sc:
                    best_sc, move = sc, (r, c)
    return move

# ── Main GUI Class ───────────────────────────────
class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe — AI Lab 06")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)
        self.board      = [['_'] * 3 for _ in range(3)]
        self.human_turn = True    # Human (O) goes first
        self.game_over  = False
        self.score      = {'You': 0, 'AI': 0, 'Draw': 0}
        self._build()

    def _build(self):
        # ── Title ──
        tk.Label(self.root, text="Tic Tac Toe", bg=BG, fg="#2c3e50",
                 font=("Arial", 20, "bold")).pack(pady=(12, 2))
        tk.Label(self.root, text="You = O (Blue)   |   AI = X (Red)",
                 bg=BG, fg="#555", font=("Arial", 11)).pack()

        # ── Score label ──
        self.score_lbl = tk.Label(self.root, text=self._score_txt(),
                                  bg=BG, font=("Arial", 11))
        self.score_lbl.pack(pady=(5, 8))

        # ── 3x3 Button Grid ──
        frame = tk.Frame(self.root, bg="#2c3e50", padx=3, pady=3)
        frame.pack()
        self.btns = []
        for r in range(3):
            row = []
            for c in range(3):
                b = tk.Button(frame, text='', font=("Arial", 36, "bold"),
                              width=4, height=2, bg=BTN_BG, relief="groove",
                              cursor="hand2",
                              command=lambda r=r, c=c: self._human(r, c))
                b.grid(row=r, column=c, padx=3, pady=3)
                row.append(b)
            self.btns.append(row)

        # ── Status & Reset button ──
        self.status = tk.Label(self.root, text="Your turn!",
                               bg=BG, fg="#2c3e50", font=("Arial", 12))
        self.status.pack(pady=(10, 4))
        tk.Button(self.root, text="New Game", font=("Arial", 11, "bold"),
                  bg=X_CLR, fg="white", relief="flat", padx=16, pady=6,
                  cursor="hand2", command=self._reset).pack(pady=(0, 14))

    # ── Human clicks a cell ──
    def _human(self, r, c):
        # Ignore if not human's turn, cell taken, or game ended
        if not self.human_turn or self.board[r][c] != '_' or self.game_over:
            return
        self._place('o', r, c)                        # Place O
        if self._check(): return                      # Check win/draw
        self.human_turn = False
        self.status.config(text="AI is thinking...", fg=X_CLR)
        self.root.after(400, self._ai)                # AI moves after 400ms

    # ── AI picks and plays its best move ──
    def _ai(self):
        r, c = best_move(self.board)                  # Minimax decision
        self._place('x', r, c)                        # Place X
        if not self._check():
            self.human_turn = True
            self.status.config(text="Your turn!", fg="#2c3e50")

    # ── Place piece on board and button ──
    def _place(self, player, r, c):
        self.board[r][c] = player
        color = X_CLR if player == 'x' else O_CLR
        self.btns[r][c].config(text=player.upper(), fg=color,
                               disabledforeground=color, state="disabled")

    # ── Check win / draw after every move ──
    def _check(self):
        sc = evaluate(self.board)
        if sc == 10:   return self._end("AI wins!", 'AI', X_CLR)
        if sc == -10:  return self._end("You win!", 'You', O_CLR)
        if not moves_left(self.board):
                       return self._end("Draw!", 'Draw', "#f39c12")
        return False

    # ── Game over: update score and ask to replay ──
    def _end(self, msg, winner, color):
        self.game_over = True
        self.score[winner] += 1
        self.score_lbl.config(text=self._score_txt())  # Refresh scoreboard
        self.status.config(text=msg, fg=color)
        if messagebox.askyesno("Game Over", f"{msg}\n\nPlay again?"):
            self._reset()
        return True

    # ── Reset board for a new round ──
    def _reset(self):
        self.board      = [['_'] * 3 for _ in range(3)]
        self.human_turn = True
        self.game_over  = False
        self.status.config(text="Your turn!", fg="#2c3e50")
        for r in range(3):
            for c in range(3):
                self.btns[r][c].config(text='', state="normal", bg=BTN_BG)

    def _score_txt(self):
        s = self.score
        return f"You: {s['You']}   Draw: {s['Draw']}   AI: {s['AI']}"
    
# ── Entry Point ──────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    TicTacToe(root)
    root.mainloop()