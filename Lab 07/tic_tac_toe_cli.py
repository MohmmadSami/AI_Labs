"""
====================================================
  LAB 06 - Tic Tac Toe  CLI Version
  Subject : Artificial Intelligence
  Run     : python3 tic_tac_toe_cli.py
====================================================
  RULES:
    You  = O  (Minimizer — tries to get LOW score)
    AI   = X  (Maximizer — tries to get HIGH score)
  SCORES:
    X wins → +10  |  O wins → -10  |  Draw → 0
====================================================
"""

import math

# ── Evaluation Function ──────────────────────────
# Checks all rows, columns, diagonals for a winner
# Returns +10 (X wins), -10 (O wins), or 0
def evaluate(b):
    lines = [
        [b[0][0], b[0][1], b[0][2]],  # Row 0
        [b[1][0], b[1][1], b[1][2]],  # Row 1
        [b[2][0], b[2][1], b[2][2]],  # Row 2
        [b[0][0], b[1][0], b[2][0]],  # Col 0
        [b[0][1], b[1][1], b[2][1]],  # Col 1
        [b[0][2], b[1][2], b[2][2]],  # Col 2
        [b[0][0], b[1][1], b[2][2]],  # Main diagonal
        [b[0][2], b[1][1], b[2][0]],  # Anti diagonal
    ]
    for line in lines:
        if line[0] == line[1] == line[2] != '_':
            return 10 if line[0] == 'x' else -10
    return 0  # No winner found

# ── Check if empty cells remain ─────────────────
def moves_left(b):
    return any(b[r][c] == '_' for r in range(3) for c in range(3))

# ── Minimax Algorithm ────────────────────────────
# Recursively tries every move to find the best one
# is_max=True → AI's turn (maximize), False → Human (minimize)
def minimax(b, depth, is_max):
    score = evaluate(b)
    if score == 10:  return score - depth  # X wins (faster win = better)
    if score == -10: return score + depth  # O wins
    if not moves_left(b): return 0         # Draw

    best = -math.inf if is_max else math.inf
    for r in range(3):
        for c in range(3):
            if b[r][c] == '_':
                b[r][c] = 'x' if is_max else 'o'       # Try the move
                val = minimax(b, depth + 1, not is_max) # Recurse
                b[r][c] = '_'                           # Undo the move
                best = max(best, val) if is_max else min(best, val)
    return best

# ── Find Best Move for AI ────────────────────────
# Tries every empty cell, scores it with minimax,
# returns the (row, col) with the highest score
def best_move(b):
    best_sc, move = -math.inf, (-1, -1)
    for r in range(3):
        for c in range(3):
            if b[r][c] == '_':
                b[r][c] = 'x'
                sc = minimax(b, 0, False)  # Score this move
                b[r][c] = '_'             # Undo
                if sc > best_sc:
                    best_sc, move = sc, (r, c)
    return move

# ── Print Board ──────────────────────────────────
# Displays the 3x3 grid with row/col index labels
def print_board(b):
    print("\n     0   1   2")
    print("   +---+---+---+")
    for i, row in enumerate(b):
        # Show each cell; use color-like markers for clarity
        cells = []
        for cell in row:
            if cell == 'x': cells.append(' X ')
            elif cell == 'o': cells.append(' O ')
            else: cells.append('   ')
        print(f" {i} |{'|'.join(cells)}|")
        print("   +---+---+---+")
    print()

# ── Get Human Input ──────────────────────────────
# Asks for row and col, validates the input
def get_human_move(b):
    while True:
        try:
            print("  Enter your move (row col) e.g. 1 2 : ", end="")
            r, c = map(int, input().split())
            if not (0 <= r <= 2 and 0 <= c <= 2):
                print("  ✗ Out of range! Use numbers 0, 1, or 2.\n")
            elif b[r][c] != '_':
                print("  ✗ Cell already taken! Choose another.\n")
            else:
                return r, c   # Valid move
        except ValueError:
            print("  ✗ Invalid input! Enter two numbers like: 1 2\n")

# ── Check Game Result ────────────────────────────
# Returns 'x', 'o', 'draw', or None if still going
def get_result(b):
    sc = evaluate(b)
    if sc == 10:  return 'x'
    if sc == -10: return 'o'
    if not moves_left(b): return 'draw'
    return None  # Game not over yet

# ── Print Score ──────────────────────────────────
def print_score(score):
    print(f"\n  Score → You (O): {score['You']}  |"
          f"  Draw: {score['Draw']}  |  AI (X): {score['AI']}")

# ── Single Game ──────────────────────────────────
# Runs one full game between Human (O) and AI (X)
def play_game(score):
    board = [['_'] * 3 for _ in range(3)]  # Fresh empty board
    human_turn = True                       # Human (O) goes first

    print("\n" + "=" * 42)
    print("   NEW GAME — You = O   |   AI = X")
    print("=" * 42)
    print("  Tip: Enter row and column (0–2) to place O")

    while True:
        print_board(board)

        # ── Check if game already ended ──
        result = get_result(board)
        if result:
            if result == 'x':
                print("  ★ AI (X) wins! Better luck next time.\n")
                score['AI'] += 1
            elif result == 'o':
                print("  ★ You (O) win! Great job!\n")
                score['You'] += 1
            else:
                print("  ★ It's a Draw!\n")
                score['Draw'] += 1
            print_score(score)
            return  # End this game

        # ── Human's Turn ──
        if human_turn:
            print("  Your turn (O):")
            r, c = get_human_move(board)  # Validated input
            board[r][c] = 'o'
            human_turn = False

        # ── AI's Turn ──
        else:
            print("  AI (X) is thinking...")
            r, c = best_move(board)       # Minimax picks best cell
            board[r][c] = 'x'
            print(f"  AI placed X at row={r}, col={c}")
            human_turn = True

# ── Main Entry Point ─────────────────────────────
def main():
    print("\n" + "=" * 42)
    print("   TIC TAC TOE  —  AI Lab 06")
    print("   Riphah University")
    print("=" * 42)
    print("  You play O (Minimizer)")
    print("  AI  plays X (Maximizer) using Minimax")

    score = {'You': 0, 'AI': 0, 'Draw': 0}  # Persist across rounds

    while True:
        play_game(score)
        print("  Play again? (y / n): ", end="")
        if input().strip().lower() != 'y':
            print("\n  Thanks for playing! Goodbye.\n")
            break

if __name__ == "__main__":
    main()