# kakuro-solver

A simple kakuro Constraint Satisfaction Problem with various backtracking methods.

Files `csp.py` `utils.py` `search.py` are forked from AIMA python repository https://github.com/aimacode/aima-python.
These files implement backtracking methods.

`kakuro.py` defines the CSP and with a class that contains the constraints, the variables, the neighbors, and the domain. 
These parameters are needed for the solution of the CSP.

##### Backtracking methods
- Backtracking
- Backtracking + MRV
- Forward check
- Forward check + MRV
- MAC
- MAC + MRV
