# latexcalc

A command-line calculator that evaluates LaTeX math expressions to numeric
values. Useful when you'd rather type `\frac{1}{6} e^{5}` than translate it
into `(1/6)*math.exp(5)` to drop into a Python REPL.

## Installation

Requires Python 3.12 and conda.

```bash
conda create -n latexcalc python=3.12
conda activate latexcalc
pip install click sympy antlr4-python3-runtime==4.11 pytest
pip install -e .
```

The `antlr4-python3-runtime==4.11` pin is required by sympy's LaTeX parser.

For convenience, alias `lc` to the env's binary so the REPL works without
needing to activate the environment:

```bash
echo "alias lc='$(conda run -n latexcalc which latexcalc)'" >> ~/.bash_profile
```

Avoid `alias lc='conda run -n latexcalc latexcalc'` — `conda run` captures
stdin, which silently breaks the interactive REPL.

## Usage

### Single-expression mode

Pass the expression as an argument; the result is printed to stdout.

```bash
$ lc '\frac{1}{6} e^{5}'
24.7355265170961

$ lc '\sin(\pi)'
0.0
```

### REPL mode

Run with no arguments to enter an interactive prompt. Quit with `exit` or
Ctrl+D.

```text
$ lc
latexcalc> \int_{0}^{1} x \, dx
0.5
latexcalc> \sum_{i=1}^{10} i
55.0
latexcalc> exit
```

## Supported expressions

| Category        | Example                       | Result        |
| --------------- | ----------------------------- | ------------- |
| Arithmetic      | `2^{10}`                      | `1024.0`      |
| Fractions       | `\frac{1}{6} e^{5}`           | `24.7355…`    |
| Roots           | `\sqrt{2}`                    | `1.4142…`     |
| Trig            | `\sin(\pi)`, `\cos(0)`        | `0.0`, `1.0`  |
| Logarithm       | `\log(e)`, `\log{e^{3}}`      | `1.0`, `3.0`  |
| Definite integrals | `\int_{0}^{1} x \, dx`     | `0.5`         |
| Summations      | `\sum_{i=1}^{10} i`           | `55.0`        |
| Constants       | `e`, `\pi`                    | symbolic      |

`e` and `\pi` are automatically substituted with their numeric values.

## Note on `\log`

`\log` is natural log (base e), not log base 10 — matching mathematical
convention rather than the programming-language convention. So `\log(e)`
is `1.0`, not `0.434…`. There is no built-in for log base 10; use
`\frac{\log(x)}{\log(10)}` if you need it.

## Limitations

- **Free variables are not supported.** Every symbol must reduce to a
  number. `x + 1` raises `Error: could not evaluate LaTeX expression
  'x + 1' to a number`.
- **The expression must be valid LaTeX.** Malformed input (e.g.
  `\frac{1}{`) raises a parse error with a caret pointing to the offending
  character.
- Both error classes exit with code 1 in single-expression mode; in REPL
  mode the error is printed and the prompt continues.
