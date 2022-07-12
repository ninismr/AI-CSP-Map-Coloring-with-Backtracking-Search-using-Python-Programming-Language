import time
from abc import ABC, abstractmethod
from json.tool import main

class Constraint(ABC):
    def __init__(self, variables):
        self.variables = variables

    @abstractmethod
    def satisfied(self, assignment):
        pass

class CSP():
    def __init__(self, variables, domains):
        self.variables = variables #variables to be constrained
        self.domains = domains #domain of each variable
        self.constraints = {}
        for variable in self.variables:
            self.constraints[variable] = []
            if variable not in self.domains:
                raise LookupError("Every variable should have a domain assigned to it.")
    
    def add_constraint(self, constraint):
        for variable in constraint.variables:
            if variable not in self.variables:
                raise LookupError("Variable in constraint not in CSP.")
            else:
                self.constraints[variable].append(constraint)
    
    def consistent(self, variable, assignment):
        for constraint in self.constraints[variable]:
            if not constraint.satisfied(assignment):
                return False
        return True
    
    def backtracking_search(self, assignment = {}):
        #assignment is complete if every variable is assigned
        if len(assignment) == len(self.variables):
            return assignment
        #get all variables in the CSP but not in the assignment
        unassigned = [v for v in self.variables if v not in assignment]
    
        #get every possible domain value of the first unassigned variable
        first = unassigned[0]
        for value in self.domains[first]:
            local_assignment = assignment.copy()
            local_assignment[first] = value
            #if we are still consistent, we recurse/continue
            if self.consistent(first, local_assignment):
                result = self.backtracking_search(local_assignment)
                #if we did not find the result, we will end up backtracking
                if result is not None:
                    return result
        return None

class MapColoringConstraint(Constraint):
    def __init__(self, region1, region2):
        super().__init__([region1, region2])
        self.region1 = region1
        self.region2 = region2
    
    def satisfied(self, assignment):
        #if either region is not in the assignment then it is not yet
        #possible for their colors to be conflicting
        if self.region1 not in assignment or self.region2 not in assignment:
            return True
        #check the color assigned to region1 is not the same as the color
        #assigned to region2
        return assignment[self.region1] != assignment[self.region2]

def new():
    new = input("Do you want to try another map (Y/N)? ")
    if new == "Y":
        main()
    elif new == "N":
        print("Thank you and have a nice day!")
        time.sleep(3)
        exit()

def main():
    variables = input("Enter the region name: ").split(',')
    variables = [i.strip() for i in variables]
    domains = {}
    domain = input("Enter the region color: ").split(',')
    domain = [i.strip() for i in domain]
    for variable in variables:
        domains[variable] = domain
        
    csp = CSP(variables, domains)
    reg = input("Enter the two adjacent regions: ").split(',')
    reg = [i.strip() for i in reg]
    csp.add_constraint(MapColoringConstraint(reg[0], reg[1]))
    
    while True:
        other = input("Do you want to add another two adjacent regions (Y/N)? ")
        if other == "Y":
            reg = input("Enter the two adjacent regions: ").split(',')
            reg = [i.strip() for i in reg]
            csp.add_constraint(MapColoringConstraint(reg[0], reg[1]))
        elif other == "N":
            solution = csp.backtracking_search()
            if solution is None:
                print("No solution has been found!")
            else:
                print("Solution: ", solution)
                new()
        else: 
            print("Please enter Y or N!")

if __name__ == "__main__":
    main()