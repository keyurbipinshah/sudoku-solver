# Importing libraries
from sys import argv
import logging
from src.utils import setup_log
from src.helpers import read_data, display_sudoku, get_output
from src.opt import build_model

def main(file_path):
    setup_log(log_level = "info")

    logging.info("Sudoku Solver initiated")

    try:
        df = read_data(file_path = file_path)
        logging.info("Unsolved Sudoku: \n\n" + display_sudoku(df = df))
    except Exception as e:
        logging.error(str(e))
        return
    
    try:
        logging.info("Building optimization model to solve the Sudoku")
        model = build_model(df = df)
        logging.info("Solving the model for a feasible solution")
        solution = get_output(model)
        logging.info("Solved Sudoku: \n\n" + display_sudoku(df = solution))
    except Exception as e:
        logging.error(str(e))
        return
        
if __name__ == "__main__":
    main(file_path = argv[1])
