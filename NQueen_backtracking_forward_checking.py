def backtracking_fc_n_queens(variables, domains, constraints):
    assignment = {}
    local_domains = {v: list(domains[v]) for v in variables}
    return recursive_backtracking_fc_n_queens(variables, assignment, local_domains, constraints)

def recursive_backtracking_fc_n_queens(variables, assignment, loc_domains, constraints):
    if len(assignment) == len(variables):
        return assignment

    variable = fc_unassign(variables, assignment)
    
    for value in list(loc_domains[variable]):
        if check_consistency(variable, value, assignment, constraints):
            # Temporarily assign variable = value
            assignment[variable] = value
            
            # Using forward checking for filtering values
            removed_values = forward_checking(variable, value, loc_domains, constraints, assignment)
            
            # Recursive
            result = recursive_backtracking_fc_n_queens(variables, assignment, loc_domains, constraints)
            if result != "Failure":
                return result

            # Backtrack: Undo assignment and restore domains
            assignment.pop(variable)
            restore_domains(removed_values, loc_domains)
            
    return 'Failure'

def forward_checking(variable, value, loc_domains, constraints, assignment):
    removed = []
    for other_variable in loc_domains:
        if other_variable not in assignment and other_variable != variable:
            new_domain = []
            for other_value in loc_domains[other_variable]:
                if (other_variable, other_value) in constraints[(variable, value)]:
                    removed.append((other_variable, other_value))
                else:
                    new_domain.append(other_value)
            loc_domains[other_variable] = new_domain
    return removed

def fc_unassign(variables, assignment):
    for variable in variables:
        if variable not in assignment:
            return variable

def check_consistency(variable, value, assignment, constraints):
    if (variable, value) in constraints[(variable, value)]:
        return False
    return True

def restore_domains(removed_values, local_domains):
    for (variable, value) in removed_values:
        local_domains[variable].append(value)