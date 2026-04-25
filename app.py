# ============================================================
#  Sudoku CSP Solver — Flask Web App
#  Algorithm : AC-3 Arc Consistency + Backtracking + MRV
#  Author    : [Your Name] | Register No: [Your Reg No]
#  Subject   : Artificial Intelligence — Problem 6
# ============================================================

from flask import Flask, render_template, request, jsonify
import time

app = Flask(__name__)

# ─────────────────────────────────────────
#  Get all peers (same row, col, 3x3 box)
# ─────────────────────────────────────────
def get_peers(row, col):
    peers = set()
    for c in range(9):
        if c != col: peers.add((row, c))
    for r in range(9):
        if r != row: peers.add((r, col))
    br, bc = (row // 3) * 3, (col // 3) * 3
    for r in range(br, br + 3):
        for c in range(bc, bc + 3):
            if (r, c) != (row, col): peers.add((r, c))
    return peers

# ─────────────────────────────────────────
#  Initialize domains for each cell
# ─────────────────────────────────────────
def initialize_domains(grid):
    domains = {}
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                domains[(r, c)] = set(range(1, 10))
            else:
                domains[(r, c)] = {grid[r][c]}
    return domains

# ─────────────────────────────────────────
#  AC-3 Arc Consistency Algorithm
# ─────────────────────────────────────────
def ac3(domains):
    queue = []
    for r in range(9):
        for c in range(9):
            for peer in get_peers(r, c):
                queue.append(((r, c), peer))
    while queue:
        (xi, xj) = queue.pop(0)
        if revise(domains, xi, xj):
            if len(domains[xi]) == 0:
                return False
            for peer in get_peers(xi[0], xi[1]):
                if peer != xj:
                    queue.append((peer, xi))
    return True

def revise(domains, xi, xj):
    revised = False
    if len(domains[xj]) == 1:
        val = next(iter(domains[xj]))
        if val in domains[xi]:
            domains[xi].discard(val)
            revised = True
    return revised

# ─────────────────────────────────────────
#  MRV Heuristic — pick most constrained cell
# ─────────────────────────────────────────
def select_unassigned(grid, domains):
    min_len, best = 10, None
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                d_len = len(domains[(r, c)])
                if d_len < min_len:
                    min_len, best = d_len, (r, c)
    return best

# ─────────────────────────────────────────
#  Constraint check
# ─────────────────────────────────────────
def is_consistent(grid, row, col, val):
    if val in grid[row]: return False
    if val in [grid[r][col] for r in range(9)]: return False
    br, bc = (row // 3) * 3, (col // 3) * 3
    for r in range(br, br + 3):
        for c in range(bc, bc + 3):
            if grid[r][c] == val: return False
    return True

# ─────────────────────────────────────────
#  Backtracking with Forward Checking
# ─────────────────────────────────────────
def backtrack(grid, domains, steps):
    cell = select_unassigned(grid, domains)
    if cell is None: return True

    row, col = cell
    for val in sorted(domains[(row, col)]):
        if is_consistent(grid, row, col, val):
            grid[row][col] = val
            steps.append({"row": row, "col": col, "val": val, "action": "place"})
            saved, conflict = {}, False
            for peer in get_peers(row, col):
                pr, pc = peer
                if grid[pr][pc] == 0 and val in domains[peer]:
                    if peer not in saved: saved[peer] = set(domains[peer])
                    domains[peer].discard(val)
                    if len(domains[peer]) == 0:
                        conflict = True; break
            if not conflict and backtrack(grid, domains, steps):
                return True
            grid[row][col] = 0
            steps.append({"row": row, "col": col, "val": 0, "action": "backtrack"})
            for peer, orig in saved.items(): domains[peer] = orig
    return False

# ─────────────────────────────────────────
#  Main solver
# ─────────────────────────────────────────
def solve_sudoku(puzzle):
    grid    = [row[:] for row in puzzle]
    domains = initialize_domains(grid)
    steps   = []
    start   = time.time()

    if not ac3(domains):
        return None, [], {"error": "No solution (AC-3 contradiction)"}

    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0 and len(domains[(r, c)]) == 1:
                grid[r][c] = next(iter(domains[(r, c)]))
                steps.append({"row": r, "col": c, "val": grid[r][c], "action": "ac3"})

    if not backtrack(grid, domains, steps):
        return None, [], {"error": "No solution exists"}

    elapsed = round((time.time() - start) * 1000, 2)
    stats = {
        "time_ms"        : elapsed,
        "steps"          : len(steps),
        "backtracks"     : sum(1 for s in steps if s["action"] == "backtrack"),
        "ac3_placements" : sum(1 for s in steps if s["action"] == "ac3"),
    }
    return grid, steps, stats

# ─────────────────────────────────────────
#  Sample puzzles
# ─────────────────────────────────────────
SAMPLE_PUZZLES = {
    "easy": [
        [5,3,0,0,7,0,0,0,0],[6,0,0,1,9,5,0,0,0],[0,9,8,0,0,0,0,6,0],
        [8,0,0,0,6,0,0,0,3],[4,0,0,8,0,3,0,0,1],[7,0,0,0,2,0,0,0,6],
        [0,6,0,0,0,0,2,8,0],[0,0,0,4,1,9,0,0,5],[0,0,0,0,8,0,0,7,9],
    ],
    "medium": [
        [0,0,0,2,6,0,7,0,1],[6,8,0,0,7,0,0,9,0],[1,9,0,0,0,4,5,0,0],
        [8,2,0,1,0,0,0,4,0],[0,0,4,6,0,2,9,0,0],[0,5,0,0,0,3,0,2,8],
        [0,0,9,3,0,0,0,7,4],[0,4,0,0,5,0,0,3,6],[7,0,3,0,1,8,0,0,0],
    ],
    "hard": [
        [0,0,0,0,0,0,0,0,0],[0,0,0,0,0,3,0,8,5],[0,0,1,0,2,0,0,0,0],
        [0,0,0,5,0,7,0,0,0],[0,0,4,0,0,0,1,0,0],[0,9,0,0,0,0,0,0,0],
        [5,0,0,0,0,0,0,7,3],[0,0,2,0,1,0,0,0,0],[0,0,0,0,4,0,0,0,9],
    ],
}

# ─────────────────────────────────────────
#  Routes
# ─────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/solve", methods=["POST"])
def solve():
    data   = request.get_json()
    puzzle = data.get("puzzle")
    if not puzzle or len(puzzle) != 9:
        return jsonify({"error": "Invalid puzzle"}), 400
    solution, steps, stats = solve_sudoku(puzzle)
    if solution is None:
        return jsonify({"error": stats.get("error", "No solution")}), 400
    return jsonify({"solution": solution, "steps": steps, "stats": stats})

@app.route("/api/sample/<difficulty>")
def sample(difficulty):
    puzzle = SAMPLE_PUZZLES.get(difficulty)
    if not puzzle:
        return jsonify({"error": "Unknown difficulty"}), 404
    return jsonify({"puzzle": puzzle})

@app.route("/api/validate", methods=["POST"])
def validate():
    data, puzzle, errors = request.get_json(), request.get_json().get("puzzle"), []
    puzzle = data.get("puzzle")
    for r in range(9):
        seen = set()
        for c in range(9):
            v = puzzle[r][c]
            if v:
                if v in seen: errors.append(f"Duplicate {v} in row {r+1}")
                seen.add(v)
    for c in range(9):
        seen = set()
        for r in range(9):
            v = puzzle[r][c]
            if v:
                if v in seen: errors.append(f"Duplicate {v} in col {c+1}")
                seen.add(v)
    for br in range(3):
        for bc in range(3):
            seen = set()
            for r in range(br*3, br*3+3):
                for c in range(bc*3, bc*3+3):
                    v = puzzle[r][c]
                    if v:
                        if v in seen: errors.append(f"Duplicate {v} in box ({br+1},{bc+1})")
                        seen.add(v)
    return jsonify({"valid": len(errors) == 0, "errors": errors})

if __name__ == "__main__":
    print("=" * 55)
    print("  Sudoku CSP Solver")
    print("  Open browser at: http://localhost:5000")
    print("=" * 55)
    app.run(debug=True, port=5000)
