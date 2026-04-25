# AI_ProblemSolving_-217-

#  Sudoku Solver (CSP)

---

##  Problem Description

This project solves a **9×9 Sudoku puzzle** where empty cells are filled such that:

* Each row contains digits **1–9 without repetition**
* Each column contains digits **1–9 without repetition**
* Each 3×3 subgrid contains digits **1–9 without repetition**

---

##  Objective

To solve Sudoku using **Artificial Intelligence techniques** by applying the **Constraint Satisfaction Problem (CSP)** approach.

---

##  Algorithm Used

**Backtracking Algorithm (CSP)**

This algorithm tries possible values and backtracks when constraints are violated.

---

##  CSP Representation

* **Variables** → Empty cells in the grid
* **Domain** → Numbers (1–9)
* **Constraints**:

  * No duplicate in row
  * No duplicate in column
  * No duplicate in 3×3 grid

---

##  Execution Steps

1. Read the Sudoku grid
2. Find an empty cell
3. Try numbers from 1 to 9
4. Check if number is valid
5. Place the number
6. Recursively solve remaining grid
7. Backtrack if needed
8. Repeat until solution is found

---

##  Sample Input

```
5 3 0 | 0 7 0 | 0 0 0
6 0 0 | 1 9 5 | 0 0 0
0 9 8 | 0 0 0 | 0 6 0
```

---

##  Sample Output

```
5 3 4 | 6 7 8 | 9 1 2
6 7 2 | 1 9 5 | 3 4 8
1 9 8 | 3 4 2 | 5 6 7
```
Website link:
     https://reshcmd3-sys.github.io/AI_ProblemSolving_-217-/
---

##  Results

* Sudoku solved successfully
* All constraints satisfied
* Efficient backtracking used

---

##  Conclusion

The Sudoku problem was solved using the **Constraint Satisfaction Problem approach**.
Backtracking ensures a correct and complete solution.

---

##  Future Enhancements

* Add GUI using Tkinter
* Add difficulty levels
* Add real-time solving visualization
