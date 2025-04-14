def backtracking_fc_mrv_lcv_n_queens(variables, domains, constraints):
    assignment = {}
    local_domains = {v: list(domains[v]) for v in variables}
    return recursive_backtracking_fc_mrv_lcv_nqueens(variables, assignment, local_domains, constraints)

def recursive_backtracking_fc_mrv_lcv_nqueens(variables, assignment, loc_domains, constraints):
    if len(assignment) == len(variables):
        return assignment

    variable = select_unassigned_variable_mrv(variables, loc_domains, assignment)
    
    for value in order_domain_values_lcv(variable, loc_domains, constraints, assignment):
        if check_consistency(variable, value, assignment, constraints):
            # Temporarily assign variable = value
            assignment[variable] = value
            
            # Using forward checking for filtering values
            removed_values = forward_checking(variable, value, loc_domains, constraints, assignment)
            
            # Recursive
            result = recursive_backtracking_fc_mrv_lcv_nqueens(variables, assignment, loc_domains, constraints)
            if result != "Failure":
                return result

            # Backtrack: Undo assignment and restore domains
            assignment.pop(variable)
            restore_domains(removed_values, loc_domains)
            
    return 'Failure'


def num_conflicts(variable, value, domains, constraints, assignment):
    counter = 0
    for other_variable in domains:
        if other_variable not in assignment and other_variable != variable:
            # For each value in neighbor's domain:
            for other_value in domains[other_variable]:
                if (other_variable, other_value) in constraints[(variable, value)]:
                    counter += 1
    return counter

def forward_checking(variable, value, domains, constraints, assignment):
    removed = []
    for other_variable in domains:
        if other_variable not in assignment and other_variable != variable:
            new_domain = []
            for other_value in domains[other_variable]:
                if (other_variable, other_value) in constraints[(variable, value)]:
                    removed.append((other_variable, other_value))
                else:
                    new_domain.append(other_value)
            domains[other_variable] = new_domain
    return removed

def select_unassigned_variable_mrv(variables, loc_domains, assignment):
    variable = [v for v in variables if v not in assignment]
    var = min(variable, key=lambda v: len(loc_domains[v]))
    return var

def check_consistency(variable, value, constraints):
    if (variable, value) in constraints[(variable, value)]:
        return False
    return True

def order_domain_values_lcv(variable, loc_domains, constraints, assignment):
    return sorted(
        loc_domains[variable],
        key=lambda val: num_conflicts(variable, val, loc_domains, constraints, assignment)
    )

def restore_domains(removed_values, domains):
    for (variable, value) in removed_values:
        domains[variable].append(value)