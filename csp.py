class CSP:

    def __init__(self, variables, domains, constraints):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints

    def get_variables(self):
        return self.variables

    def get_domains(self):
        return self.domains
    
    def get_constraints(self):
        return self.constraints

    def set_variables(self, variables):
        self.variables = variables

    def set_domains(self, domains):
        self.domains = domains
       
    def set_constraints(self, constraints):
        self.constraints = constraints
    
    def __str__(self):
        return f"Variables: {self.variables}\nDomains: {self.domains}\nConstarints: {self.constraints}"
