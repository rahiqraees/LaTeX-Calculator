import sympy
from sympy.parsing.latex import parse_latex
from sympy.parsing.latex.errors import LaTeXParsingError

CONSTANTS = {
    sympy.Symbol("e"): sympy.E,
    sympy.Symbol("pi"): sympy.pi,
}


def evaluate(expr: str) -> float:
    try:
        parsed = parse_latex(expr)
    except LaTeXParsingError as exc:
        raise ValueError(f"could not parse LaTeX expression {expr!r}: {exc}") from exc
    substituted = parsed.subs(CONSTANTS)
    return float(sympy.N(substituted.doit()))
