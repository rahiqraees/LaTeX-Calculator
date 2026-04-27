import math

import pytest

from latexcalc.evaluator import evaluate


def test_evaluates_frac_one_sixth_times_e_to_the_fifth():
    result = evaluate(r"\frac{1}{6} e^{5}")
    assert math.isclose(result, math.exp(5) / 6, rel_tol=1e-9)


def test_evaluates_sin_of_pi_to_zero():
    result = evaluate(r"\sin(\pi)")
    assert math.isclose(result, 0.0, abs_tol=1e-12)


def test_invalid_latex_raises_value_error_with_expression_in_message():
    bad = r"\frac{1}{"
    with pytest.raises(ValueError) as exc_info:
        evaluate(bad)
    assert bad in str(exc_info.value)
