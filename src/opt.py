# Importing libraries
import pandas as pd
import gurobipy as gp
from itertools import product
import logging

# Defining Gurobi environment and suppressing output
env = gp.Env()
env.setParam("OutputFlag", 0)

# Function that builds the optimization model
def build_model(df):

    model = gp.Model("sudoku_solver", env = env)

    logging.info("Adding decision variables to the model")
    n = range(1, 9 + 1)
    ind = product(n, n, n)    
    x = model.addVars(ind, vtype = gp.GRB.BINARY, name = "x")

    logging.info("Adding constraints for input cells")
    for i, j in product(n, n):
        if df.loc[i, j] is not pd.NA:
            lin_expr = x.select(i, j, df.loc[i, j])[0] == 1
            model.addConstr(lin_expr)

    logging.info("Adding constraints that each cell can only have one number")
    for i, j in product(n, n):
        lin_expr = x.sum(i, j, "*") == 1
        model.addConstr(lin_expr)

    logging.info("Adding constraints that every column must have exactly one cell for each number")
    for j, k in product(n, n):
        lin_expr = x.sum("*", j, k) == 1
        model.addConstr(lin_expr)

    logging.info("Adding constraints that every row must have exactly one cell for each number")
    for i, k in product(n, n):
        lin_expr = x.sum(i, "*", k) == 1
        model.addConstr(lin_expr)

    logging.info("Adding constraints that every non-overlapping 3 x 3 sub-grids must have exactly one cell for each number") 
    for i, j in product([1, 4, 7], [1, 4, 7]):
        for k in n:
            lin_expr = gp.LinExpr(0)
            for i_prime in range(i, i + 3):
                for j_prime in range(j, j + 3):
                    lin_expr.addTerms(1, x.select(i_prime, j_prime, k)[0])
            model.addConstr(lin_expr == 1)

    logging.info("Setting a constant model objective since we only need to find a feasible solution")
    model.ModelSense = gp.GRB.MINIMIZE
    model.setObjective(1)

    return model