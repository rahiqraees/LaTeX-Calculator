# LaTeX Calculator (latexcalc)

A CLI tool that takes LaTeX math expressions as input and returns numerical results.
Motivation: type `\frac{1}{6} e^{5}` instead of `(1/6)*np.exp(5)` in a Python REPL.

## Stack
- Python 3.12
- conda environment: `latexcalc`
- CLI: click
- Math: sympy + antlr4-python3-runtime==4.11 (version pin is required)
- Tests: pytest

## Installation
```bash
conda create -n latexcalc python=3.12
conda activate latexcalc
pip install click sympy antlr4-python3-runtime==4.11 pytest
```

## Running tests
```bash
pytest
```

## Evaluation pipeline
parse_latex(expr) -> .subs(constants) -> .doit() -> N()

Constants that require explicit substitution post-parse:
- `e` -> sympy.E (Euler's number)
- `pi` -> sympy.pi (parse_latex emits Symbol('pi'), which prints identically to sympy.pi but won't simplify under N())
- more to be discovered and added here

## Milestones
1. MVP: single expression in, numerical result out
   `latexcalc "\frac{1}{6} e^{5}"` prints `24.8...`
2. Next: interactive REPL mode

## Conventions
- Keep functions pure where possible
- Core evaluation logic lives separately from CLI code
- New constants and edge cases get a test before a fix