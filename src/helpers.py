# Importing libraries
import pandas as pd
import logging

# Function that displays the sudoku board
def display_sudoku(df):
    df_dict = df.to_dict(orient = "index")
    output = ""
    for row_id in df_dict.keys():
        for column_id in df_dict[row_id].keys():
            output += str(df_dict[row_id][column_id]) if df_dict[row_id][column_id] is not None else "X"
            output += " "
            if column_id in [3, 6]:
                output += "| "
        output += "\n"
        if row_id in [3, 6]:
            output += "------+-------+------\n"

    return output

# Function to read input data and format the column and index names
def read_data(file_path):

    n = [*range(1, 9 + 1)]
    
    logging.info("Reading unsolved Sudoku")
    df = pd.read_csv(file_path, dtype = "Int64", index_col = 0)
    df.index = n
    df.columns = n

    return df

# Function that organises the output
def get_output(model):

    logging.info("Optimizing the model")
    model.optimize()

    logging.info("Getting model solution")
    var_names = model.getAttr("VarName", model.getVars())
    var_names = [tuple(iter.replace("x[", "").replace("]", "").split(",")) for iter in var_names]
    var_values = model.getAttr("X", model.getVars())
    var_values = {iter[0]: iter[1] for iter in [*zip(var_names, var_values)]}

    logging.info("Formatting model output")
    solution = pd.Series(var_values).reset_index()
    solution.columns = ["row_id", "column_id", "number", "flag"]
    solution = solution[solution.flag == 1].drop(columns = ["flag"])
    solution = solution.astype("Int64")
    solution = solution.pivot(index = "row_id", columns = "column_id", values = "number")
    solution.index.name = None
    solution.columns.name = None

    return solution