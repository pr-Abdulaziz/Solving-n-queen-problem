# N-Queens Problem Solver

> A comprehensive implementation and comparative analysis of exact and metaheuristic algorithms for the N‑Queens problem.

**Student:** Abdulaziz Alqahtani  
**Student ID:** 202283240  
**Course:** ICS381 – Programming Assignment 2 (Term 242)

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Getting Started](#getting-started)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
3. [Repository Structure](#repository-structure)
4. [Algorithms Detailed](#algorithms-detailed)
   - [Part A: Exact Search Methods (CSP)](#part-a-exact-search-methods-csp)
     - [1. Simple Backtracking](#1-simple-backtracking)
     - [2. Forward Checking](#2-forward-checking)
     - [3. MRV + LCV + Forward Checking](#3-mrv--lcv--forward-checking)
   - [Part B: Simulated Annealing](#part-b-simulated-annealing)
   - [Part C: Genetic Algorithm](#part-c-genetic-algorithm)
5. [Benchmark Harness](#benchmark-harness)
   - [Configuration](#configuration)
   - [Running Benchmarks](#running-benchmarks)
   - [Sample Output](#sample-output)
6. [Appendix: Source Modules](#appendix-source-modules)
7. [Contributing](#contributing)
8. [License](#license)

---

## Project Overview

The **N-Queens problem** asks: How can you place **N** queens on an **N×N** chessboard so that none can attack another (no two share the same row, column, or diagonal)?

This project explores five solution strategies:

- **Exact Search (CSP-based):**
  1. Backtracking
  2. Backtracking + Forward Checking
  3. Backtracking + MRV & LCV Heuristics + Forward Checking
- **Metaheuristics:**
  4. Simulated Annealing
  5. Genetic Algorithm

Each method is implemented in Python, integrated into a common test harness that measures average runtimes over multiple trials for board sizes **N = 4, 8, 10, 15, 20, 24, 27**.

The accompanying report analyzes correctness, time complexity, and performance trade‑offs.

---

## Getting Started

### Prerequisites

- **Python 3.7+**
- Standard library modules only (`random`, `math`, `time`, etc.)

### Installation

```bash
# Clone the repository
git clone https://github.com/<your-username>/nqueen-solver.git
cd nqueen-solver

# (Optional) Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
```

---

## Repository Structure

```
├── csp.py                          # Core CSP class (variables, domains, constraints)
├── NQueen_backtracking.py          # 1. Simple Backtracking implementation
├── NQueen_backtracking_forward_checking.py  # 2. Forward Checking enhancement
├── NQueen_MRV_LCV.py               # 3. MRV & LCV heuristics + FC
├── other_alg_n_queen_problem/
│   ├── NQueenProblem.py            # State & cost for Simulated Annealing
│   ├── NQueen_simulated_annealing.py  # SA algorithm with cooling schedule
│   ├── NQueenProblem_GA.py         # State & fitness for Genetic Algorithm
│   └── genetic_alg.py              # GA main loop (selection, crossover, mutation)
├── test.py                         # Benchmark harness (runs & times all algorithms)
└── README.md                       # Project overview and instructions
```

---

## Algorithms Detailed

### Part A: Exact Search Methods (CSP)

All exact methods model N-Queens as a **Constraint Satisfaction Problem (CSP)**:

- **Variables:** Columns Q1…QN
- **Domains:** Row indices {1…N}
- **Constraints:** For any two variables (Qi, Qj), their assigned rows must not be equal (no same row) and must not lie on the same diagonal (|row_i – row_j| ≠ |i – j|).

#### 1. Simple Backtracking

- **Module:** `NQueen_backtracking.py`
- **Approach:** Depth-first recursive assignment of columns. On each step:
  1. Pick the next unassigned column.
  2. Try each row in its domain.
  3. Check consistency against existing assignments.
  4. If conflict, backtrack and try next row.

<details>
<summary>Pseudocode</summary>

```text
function backtrack(assignment):
  if all columns assigned: return assignment
  var = select_unassigned_column()
  for row in domain[var]:
    if is_consistent(var, row, assignment):
      assignment[var] = row
      result = backtrack(assignment)
      if result != failure: return result
      remove assignment[var]
  return failure
```
</details>

**Time Complexity:** O(N!), impractical beyond small N.

#### 2. Forward Checking

- **Module:** `NQueen_backtracking_forward_checking.py`
- **Enhancement:** After assigning a row to Qi, immediately **prune** incompatible rows from the domains of all unassigned Qj. This prevents deeper futile searches.

<details>
<summary>Key Steps</summary>

1. Assign Qi = r.
2. For each unassigned Qj, remove rows that conflict with (Qi, r).
3. Recurse with reduced domains.
4. On backtrack, **restore** pruned values.
</details>

**Benefit:** Reduces search tree size significantly.

#### 3. MRV & LCV + Forward Checking

- **Module:** `NQueen_MRV_LCV.py`
- **Heuristics:**
  - **MRV (Minimum Remaining Values):** Choose the next column with the smallest current domain.
  - **LCV (Least Constraining Value):** Order row assignments by how few conflicts they introduce for remaining columns.

Combining MRV and LCV guides the search toward promising paths and delays dead ends.

---

### Part B: Simulated Annealing

- **Modules:**
  - `other_alg_n_queen_problem/NQueenProblem.py`
  - `other_alg_n_queen_problem/NQueen_simulated_annealing.py`

**State Representation:** Array `state[0…N-1]`, where `state[i] = row` of queen in column i.

**Cost Function:** Number of attacking pairs (to minimize).

**Neighbor Generation:** Change the row of a single column to any other row.

**Algorithm Outline:**

1. **Initialize** with a random (or greedy) state.
2. For t = 1… until temperature ≈ 0:
   - T = schedule(t) (e.g., `T0 * alpha^t`)
   - Pick a random neighbor.
   - Δ = cost(current) – cost(neighbor)
   - If Δ > 0, **accept** neighbor.
   - Else accept with probability `exp(Δ / T)`.
3. Return current state when cooled.

**Advantage:** Escapes local minima; scales to large N quickly.

---

### Part C: Genetic Algorithm

- **Modules:**
  - `other_alg_n_queen_problem/NQueenProblem_GA.py`
  - `other_alg_n_queen_problem/genetic_alg.py`

**Chromosome:** Array of length N; each gene = row of queen in that column.

**Fitness:** Negative of number of attacking pairs (higher = better).

**Operators:**

- **Selection:** Weighted random selection by fitness.
- **Crossover:** Single-point crossover between two parents.
- **Mutation:** Randomly change one gene (row) in the offspring.

**Loop:**
1. Generate initial population.
2. Evaluate fitness.
3. While no perfect solution and generations remain:
   - Select parents.
   - Produce children via crossover + mutation.
   - Form new population.
4. Return best chromosome.

**Advantage:** Parallel exploration of search space; good for very large N.

---

## Benchmark Harness

All algorithms are timed and compared in `test.py`.

### Configuration

- **Board sizes:** N = [4, 8, 10, 15, 20, 24, 27]
- **Trials per N:** 4 (average runtime reported)

### Running Benchmarks

```bash
python test.py
```

### Sample Output

```text
Running each algorithm 4 times per n.
 n | Backtrack |        FC |  FC+MRV+LCV |        SA |        GA
-------------------------------------------------------------------
  4 |     0.0001 |     0.0002 |      0.0003 |     0.0015 |     0.0020
  8 |     0.0020 |     0.0010 |      0.0008 |     0.0050 |     0.0070
 15 |     0.1500 |     0.0200 |      0.0150 |     0.0250 |     0.0300
 27 |     3.5000 |     0.5000 |      0.2000 |     0.1000 |     0.1200
Done.
```

---

## Appendix: Source Modules

- **csp.py**: CSP class with `variables`, `domains`, `constraints` management.
- **NQueen_backtracking.py**: Basic backtracking solver.
- **NQueen_backtracking_forward_checking.py**: FC-enhanced backtracking.
- **NQueen_MRV_LCV.py**: MRV & LCV heuristics + FC.
- **other_alg_n_queen_problem/NQueenProblem.py**: SA state and cost.
- **other_alg_n_queen_problem/NQueen_simulated_annealing.py**: SA algorithm.
- **other_alg_n_queen_problem/NQueenProblem_GA.py**: GA state and fitness.
- **other_alg_n_queen_problem/genetic_alg.py**: GA operators and loop.
- **test.py**: Benchmark runner and timer.

---

## Contributing

Contributions, bug reports, and feature requests are welcome! Please fork the repo and submit a pull request.

---

## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE. See [LICENSE](LICENSE) for details.

