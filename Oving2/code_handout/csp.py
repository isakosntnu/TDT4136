from typing import Any
from queue import Queue

from collections import deque


class CSP:
    def __init__(
        self,
        variables: list[str],
        domains: dict[str, set],
        edges: list[tuple[str, str]],
    ):
        """Constructs a CSP instance with the given variables, domains and edges.
        
        Parameters
        ----------
        variables : list[str]
            The variables for the CSP
        domains : dict[str, set]
            The domains of the variables
        edges : list[tuple[str, str]]
            Pairs of variables that must not be assigned the same value
        """
        self.variables = variables
        self.domains = domains

        # Binary constraints as a dictionary mapping variable pairs to a set of value pairs.
        #
        # To check if variable1=value1, variable2=value2 is in violation of a binary constraint:
        # if (
        #     (variable1, variable2) in self.binary_constraints and
        #     (value1, value2) not in self.binary_constraints[(variable1, variable2)]
        # ) or (
        #     (variable2, variable1) in self.binary_constraints and
        #     (value1, value2) not in self.binary_constraints[(variable2, variable1)]
        # ):
        #     Violates a binary constraint
        self.binary_constraints: dict[tuple[str, str], set] = {}
        for variable1, variable2 in edges:
            self.binary_constraints[(variable1, variable2)] = set()
            for value1 in self.domains[variable1]:
                for value2 in self.domains[variable2]:
                    if value1 != value2:
                        self.binary_constraints[(variable1, variable2)].add((value1, value2))
                        self.binary_constraints[(variable1, variable2)].add((value2, value1))

    def ac_3(self):
        """Performs AC-3 on the CSP.
        Meant to be run prior to calling backtracking_search() to reduce the search for some problems.
        
        Returns
        -------
        bool
            False if a domain becomes empty, otherwise True
        """
        queue = deque(self.binary_constraints.keys())

        while queue:
            (xi, xj) = queue.popleft()
            if self.revise(xi, xj):
                if not self.domains[xi]:
                    return False 
                for xk in self.get_neighbors(xi):
                    if xk != xj:
                        queue.append((xk, xi))
        return True

    def revise(self, xi, xj):
        revised = False
        for x in self.domains[xi].copy():
            if all(not self.constraints(xi, x, xj, y) for y in self.domains[xj]):
                self.domains[xi].remove(x)
                revised = True
        return revised

    def get_neighbors(self, var):
        neighbors = set()
        for (xi, xj) in self.binary_constraints:
            if xi == var:
                neighbors.add(xj)
            elif xj == var:
                neighbors.add(xi)
        return neighbors

    def constraints(self, var1, value1, var2, value2):
        if (var1, var2) in self.binary_constraints:
            return (value1, value2) in self.binary_constraints[(var1, var2)]
        elif (var2, var1) in self.binary_constraints:
            return (value2, value1) in self.binary_constraints[(var2, var1)]
        else:
            return True

    def backtracking_search(self):
        return self.backtrack({})

    def backtrack(self, assignment):
        if len(assignment) == len(self.variables):
            return assignment
        
        var = self.select_unassigned_variable(assignment)
        
        for value in self.order_domain_values(var, assignment):
            if self.is_consistent(var, value, assignment):
                assignment[var] = value
                
                result = self.backtrack(assignment)
                if result:
                    return result
                
                del assignment[var]
        
        return None  

    def select_unassigned_variable(self, assignment):
        return [v for v in self.variables if v not in assignment][0]

    def order_domain_values(self, var, assignment):
        return list(self.domains[var])

    def is_consistent(self, var, value, assignment):
        for neighbor in self.get_neighbors(var):
            if neighbor in assignment and not self.constraints(var, value, neighbor, assignment[neighbor]):
                return False
        return True


def alldiff(variables: list[str]) -> list[tuple[str, str]]:
    """Returns a list of edges interconnecting all of the input variables
    
    Parameters
    ----------
    variables : list[str]
        The variables that all must be different

    Returns
    -------
    list[tuple[str, str]]
        List of edges in the form (a, b)
    """
    return [(variables[i], variables[j]) for i in range(len(variables) - 1) for j in range(i + 1, len(variables))]

from typing import Any
from queue import Queue

from collections import deque


class CSP:
    def __init__(
        self,
        variables: list[str],
        domains: dict[str, set],
        edges: list[tuple[str, str]],
    ):
        """Constructs a CSP instance with the given variables, domains and edges.
        
        Parameters
        ----------
        variables : list[str]
            The variables for the CSP
        domains : dict[str, set]
            The domains of the variables
        edges : list[tuple[str, str]]
            Pairs of variables that must not be assigned the same value
        """
        self.variables = variables
        self.domains = domains

        # Binary constraints as a dictionary mapping variable pairs to a set of value pairs.
        #
        # To check if variable1=value1, variable2=value2 is in violation of a binary constraint:
        # if (
        #     (variable1, variable2) in self.binary_constraints and
        #     (value1, value2) not in self.binary_constraints[(variable1, variable2)]
        # ) or (
        #     (variable2, variable1) in self.binary_constraints and
        #     (value1, value2) not in self.binary_constraints[(variable2, variable1)]
        # ):
        #     Violates a binary constraint
        self.binary_constraints: dict[tuple[str, str], set] = {}
        for variable1, variable2 in edges:
            self.binary_constraints[(variable1, variable2)] = set()
            for value1 in self.domains[variable1]:
                for value2 in self.domains[variable2]:
                    if value1 != value2:
                        self.binary_constraints[(variable1, variable2)].add((value1, value2))
                        self.binary_constraints[(variable1, variable2)].add((value2, value1))

    def ac_3(self):
        """Performs AC-3 on the CSP.
        Meant to be run prior to calling backtracking_search() to reduce the search for some problems.
        
        Returns
        -------
        bool
            False if a domain becomes empty, otherwise True
        """
        queue = deque(self.binary_constraints.keys())

        while queue:
            (xi, xj) = queue.popleft()
            if self.revise(xi, xj):
                if not self.domains[xi]:
                    return False 
                for xk in self.get_neighbors(xi):
                    if xk != xj:
                        queue.append((xk, xi))
        return True

    def revise(self, xi, xj):
        revised = False
        for x in self.domains[xi].copy():
            if all(not self.constraints(xi, x, xj, y) for y in self.domains[xj]):
                self.domains[xi].remove(x)
                revised = True
        return revised
    

    def get_neighbors(self, var):
        neighbors = set()
        for (xi, xj) in self.binary_constraints:
            if xi == var:
                neighbors.add(xj)
            elif xj == var:
                neighbors.add(xi)
        return neighbors

    def constraints(self, var1, value1, var2, value2):
        if (var1, var2) in self.binary_constraints:
            return (value1, value2) in self.binary_constraints[(var1, var2)]
        elif (var2, var1) in self.binary_constraints:
            return (value2, value1) in self.binary_constraints[(var2, var1)]
        else:
            return True

     # Initialize counters
    backtrack_calls = 0
    backtrack_failures = 0

def backtracking_search_with_counts(csp):
    """Performs backtracking search and counts the number of calls and failures."""
    from time import time

    # Use nonlocal variables to modify counters within nested function
    counters = {'calls': 0, 'failures': 0}

    def backtrack(assignment):
        counters['calls'] += 1

        # If assignment is complete, return it
        if len(assignment) == len(csp.variables):
            return assignment

        # Select an unassigned variable
        var = csp.select_unassigned_variable(assignment)

        # Try each possible value in the domain
        for value in csp.order_domain_values(var, assignment):
            if csp.is_consistent(var, value, assignment):
                assignment[var] = value

                # Recursive call
                result = backtrack(assignment)
                if result:
                    return result

                # Backtrack
                del assignment[var]

        # Increment failure counter
        counters['failures'] += 1
        return None  # Failure

    # Measure the runtime of backtracking search
    start_time = time()
    result = backtrack({})
    end_time = time()
    runtime = end_time - start_time

    # Return the result and statistics
    return result, counters['calls'], counters['failures'], runtime 

    def select_unassigned_variable(self, assignment):
        return [v for v in self.variables if v not in assignment][0]

    def order_domain_values(self, var, assignment):
        return list(self.domains[var])

    def is_consistent(self, var, value, assignment):
        for neighbor in self.get_neighbors(var):
            if neighbor in assignment and not self.constraints(var, value, neighbor, assignment[neighbor]):
                return False
        return True


def alldiff(variables: list[str]) -> list[tuple[str, str]]:
    """Returns a list of edges interconnecting all of the input variables
    
    Parameters
    ----------
    variables : list[str]
        The variables that all must be different

    Returns
    -------
    list[tuple[str, str]]
        List of edges in the form (a, b)
    """
    return [(variables[i], variables[j]) for i in range(len(variables) - 1) for j in range(i + 1, len(variables))]
