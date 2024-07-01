# SATSolver

A powerful SAT solver that dynamically uses different strategies to solve SAT problems.

## Overview

The SATSolver is a tool for solving SAT problems (Boolean Satisfiability Problems). Depending on the given formula, the solver dynamically selects the most suitable strategy for solving the problem. The following strategies are implemented:

- **2KNF (2-CNF)**: Solution for formulas in conjunctive normal form with a maximum of two literals per clause.
- **DNF-SAF**: Solution for formulas in disjunctive normal form.
- **Resolution**: A general procedure for solving SAT problems using resolution rules.
- **DPLL (Davis-Putnam-Logemann-Loveland)**: A recursive algorithm for decidability of SAT problems.
- **Hyperresolution**: An extension of the resolution technique for larger clauses.
- **Marking algorithm**: An algorithm for identifying satisfiability by marking variables.

## Installation

1. clone the repository:
    ```sh
    git clone https://github.com/Zemux1613/SATSolver.git
    ```
2. go to the project directory:
    ```sh
    cd SATSolver
    ```
3. install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

The SATSolver can be executed via the command line. Here is an example of how to use the solver with an input formula:

```sh
python SATSolver.py "your_formula"
```
