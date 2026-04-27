import math

from click.testing import CliRunner

from latexcalc.cli import main


def test_cli_prints_numerical_result():
    runner = CliRunner()
    result = runner.invoke(main, [r"\frac{1}{6} e^{5}"])

    assert result.exit_code == 0
    printed = float(result.output.strip())
    assert math.isclose(printed, math.exp(5) / 6, rel_tol=1e-9)


def test_cli_prints_clean_error_on_invalid_latex():
    runner = CliRunner()
    result = runner.invoke(main, [r"\frac{1}{"])

    assert result.exit_code == 1
    assert result.output.startswith("Error:")
    assert "Traceback" not in result.output
    assert r"\frac{1}{" in result.output
