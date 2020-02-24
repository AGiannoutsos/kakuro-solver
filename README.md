# kakuro-solver

A simple kakuro Constraint Satisfaction Problem with various backtracking methods.

Files `csp.py` `utils.py` `search.py` are forked from AIMA python repository https://github.com/aimacode/aima-python.
These files implement backtracking methods.

`kakuro.py` defines the CSP and with a class that contains the constraints, the variables, the neighbors, and the domain. 
These parameters are needed for the solution of the CSP.


#### About the Constraints
There are 3 binary constraints that the program tries to satisfy.

1. 2 neighbor variables cant be equal
2. The sum of an array must be equal to its constrain
3. If in an array only 2 variables are assigned then their sum must be less than the constraint of the array


#### Backtracking methods
- Backtracking
- Backtracking + MRV
- Forward check
- Forward check + MRV
- MAC
- MAC + MRV


#### Results


