# Instructions to use the Sudoku Solver

### Clone the repository
Install `git` in local and run the following git command in command line wherever you want to store the code:  
```
git clone https://github.com/keyurbipinshah/sudoku-solver.git
```

### Set up Python environment
Install Python 3.11.0 in local, navigate to the `sudoku-solver` folder and run the following commands in command line to set up the Python environment:  
```
python -m venv venv  
venv\Scripts\python.exe -m pip install -r requirements.txt 
```  

### Update `sudoku.csv` to the problem you want to solve
1. First row of the file represents the column indices (1, 2, ..., 9)
2. Blank values in the file represent the values that the solver will determine  

### Run the solver in command line
Run the following command in command line to run the solver  
```
venv\Scripts\python.exe run.py sudoku.csv
```
