import time
from csp import CSP
from NQueen_backtracking import backtracking_search_n_queens
from NQueen_backtracking_forward_checking import backtracking_fc_n_queens
from NQueen_MRV_LCV import backtracking_fc_mrv_lcv_n_queens
# Import Simulated Annealing
from other_alg_n_queen_problem.NQueenProblem import NQueen
from other_alg_n_queen_problem.NQueen_simulated_annealing import simulated_annealing, schedule
# Import Genetic Algorithm
from other_alg_n_queen_problem.NQueenProblem_GA import NQueenGA
from other_alg_n_queen_problem.genetic_alg import solve

def run_and_time(func, variables, domains, constraints, trials):
    times = []
    sol_sample = None
    for _ in range(trials):
        start = time.time()
        sol = func(variables, domains, constraints)
        end = time.time()
        times.append(end - start)
        # store last solution as sample
        sol_sample = sol
    return (sum(times)/len(times), sol_sample)

def run_and_time_for_sim(func, problem, trials):
    times = []
    sol_sample = None
    for _ in range(trials):
        start = time.time()
        sol = func(problem, schedule)
        end = time.time()
        times.append(end - start)
        # store last solution as sample
        sol_sample = sol
    return (sum(times)/len(times), sol_sample)


def run_and_time_for_gen(func, problem, trials):
    times = []
    sol_sample = None
    for _ in range(trials):
        start = time.time()
        sol = func(problem)
        end = time.time()
        times.append(end - start)
        # store last solution as sample
        sol_sample = sol
    return (sum(times)/len(times), sol_sample)


def csp(n):
    variables = [f"Q{i}" for i in range(1, n+1)]
    domains = {var: list(range(1, n+1)) for var in variables}
    # Build a threat map for each (var, row).
    constraints = add_constraints(n)
    return CSP(variables, domains, constraints)


def add_constraints(n):
    
    constraints = {}
    for col in range(1, n+1):
        var = f"Q{col}"
        for row in range(1, n+1):
            key = (var, row)
            threatened = []

            # Same row for other columns
            for other_col in range(1, n+1):
                if other_col != col:
                    threatened.append((f"Q{other_col}", row))
            
            # Diagonals
            for delta in range(1, n):
                # Down-right diagonal
                if col + delta <= n and row + delta <= n:
                    threatened.append((f"Q{col + delta}", row + delta))
                # Up-left diagonal
                if col - delta >= 1 and row - delta >= 1:
                    threatened.append((f"Q{col - delta}", row - delta))
                # Down-left diagonal
                if col - delta >= 1 and row + delta <= n:
                    threatened.append((f"Q{col - delta}", row + delta))
                # Up-right diagonal
                if col + delta <= n and row - delta >= 1:
                    threatened.append((f"Q{col + delta}", row - delta))
            
            constraints[key] = threatened
    return constraints
    
def main():
    
    ns = [4, 8, 10, 15, 20, 24, 27]
    trials = 4

    print(f"Running each algorithm {trials} times per n.\n")

    print(f"{'n':>3s} | {'Backtrack':>10s} | {'FC':>10s} | {'FC+MRV+LCV':>12s} | {'SA':>10s} | {'GA':>10s}")
    print("-"*75)
    for n in ns:
        def_csp = csp(n)
        variables = def_csp.get_variables()
        domains = def_csp.get_domains()
        constraints = def_csp.get_constraints()
        t_back, _ = run_and_time(backtracking_search_n_queens, variables, domains, constraints, trials)
        t_fc, _= run_and_time(backtracking_fc_n_queens, variables, domains, constraints, trials)
        t_fc_mrv_lcv, _= run_and_time(backtracking_fc_mrv_lcv_n_queens, variables, domains, constraints, trials)
        # Simulated Annealing & Genetic Algorithm
        problem = NQueen(n)
        genetic_alg_problem = NQueenGA(n)
        t_sim_an, _ = run_and_time_for_sim(simulated_annealing, problem, trials)
        t_genetic_alg, _ = run_and_time_for_gen(solve, genetic_alg_problem, trials)
        
        print(f"{n:3d} | {t_back:10.4f} | {t_fc:10.4f} | {t_fc_mrv_lcv:12.4f} | {t_sim_an:10.4f} | {t_genetic_alg:10.4f}")

    print("\nDone.")

if __name__ == "__main__":
    main()
