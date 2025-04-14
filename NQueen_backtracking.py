def backtracking_search_n_queens(variables, domains, constraints):
    assignment = {}
    solution = backtrack(variables, domains, constraints, assignment)
    return solution

def backtrack(variables, domains, constraints, assignment):
    variables = list(variables)
    if (len(assignment) == len(variables)):
        return assignment

    variable = unassigned_variables(variables, assignment)
    
    for value in order_domain_values(domains, variable):
        if check_consistency(variable, constraints, value, assignment):
            assignment[variable] = value
            result = backtrack(variables, domains, constraints, assignment)
            if result != "Failure":
                return result
            
            assignment.pop(variable)
      
    return 'Failure'

def unassigned_variables(variables, assignment):
    for variable in variables:
        if variable not in assignment:
            return variable

def order_domain_values(domains, variable):
    return list(domains[variable])

def check_consistency(variable, constraints, value, assignment):
    for var2, row2 in assignment.items():
        if (var2, row2) in constraints[(variable, value)]:
            return False

    return True
    
