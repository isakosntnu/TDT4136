# Sudoku problems.
# The CSP.ac_3() and CSP.backtrack() methods need to be implemented

import time
from csp import CSP, alldiff, backtracking_search_with_counts


def print_solution(solution):
    """
    Convert the representation of a Sudoku solution, as returned from
    the method CSP.backtracking_search(), into a Sudoku board.
    """
    for row in range(width):
        for col in range(width):
            print(solution[f'X{row+1}{col+1}'], end=" ")
            if col == 2 or col == 5:
                print('|', end=" ")
        print("")
        if row == 2 or row == 5:
            print('------+-------+------')


# Choose Sudoku problem
grid = open('sudoku_easy.txt').read().split()

width = 9
box_width = 3

domains = {}
for row in range(width):
    for col in range(width):
        if grid[row][col] == '0':
            domains[f'X{row+1}{col+1}'] = set(range(1, 10))
        else:
            domains[f'X{row+1}{col+1}'] = {int(grid[row][col])}

edges = []
for row in range(width):
    edges += alldiff([f'X{row+1}{col+1}' for col in range(width)])
for col in range(width):
    edges += alldiff([f'X{row+1}{col+1}' for row in range(width)])
for box_row in range(box_width):
    for box_col in range(box_width):
        cells = []
        edges += alldiff(
            [
                f'X{row+1}{col+1}' for row in range(box_row * box_width, (box_row + 1) * box_width)
                for col in range(box_col * box_width, (box_col + 1) * box_width)
            ]
        )

csp = CSP(
    variables=[f'X{row+1}{col+1}' for row in range(width) for col in range(width)],
    domains=domains,
    edges=edges,
)

# Run AC-3 algorithm and measure runtime
ac3_start_time = time.time()
ac3_result = csp.ac_3()
ac3_end_time = time.time()
ac3_runtime = ac3_end_time - ac3_start_time

print(csp.ac_3())
if ac3_result:
    print("Domains after AC-3:")
    for var in sorted(csp.variables):
        print(f"{var}: {csp.domains[var]}")

    backtrack_calls = 0
    backtrack_failures = 0

    solution, backtrack_calls, backtrack_failures, backtracking_runtime = backtracking_search_with_counts(csp)
    total_runtime = ac3_runtime + backtracking_runtime

    print(f"Backtrack calls: {backtrack_calls}")
    print(f"Backtrack failures: {backtrack_failures}")
    print(f"Backtracking runtime: {backtracking_runtime:.6f} seconds")
    print(f"AC-3 runtime: {ac3_runtime:.6f} seconds")
    print(f"Total runtime: {total_runtime:.6f} seconds")

    print_solution(csp.backtracking_search())
else:
    print("No solution found during AC-3 preprocessing.")
print_solution(csp.backtracking_search())

# Expected output after implementing csp.ac_3() and csp.backtracking_search():
# True
# 7 8 4 | 9 3 2 | 1 5 6
# 6 1 9 | 4 8 5 | 3 2 7
# 2 3 5 | 1 7 6 | 4 8 9
# ------+-------+------
# 5 7 8 | 2 6 1 | 9 3 4
# 3 4 1 | 8 9 7 | 5 6 2
# 9 2 6 | 5 4 3 | 8 7 1
# ------+-------+------
# 4 5 3 | 7 2 9 | 6 1 8
# 8 6 2 | 3 1 4 | 7 9 5
# 1 9 7 | 6 5 8 | 2 4 3
