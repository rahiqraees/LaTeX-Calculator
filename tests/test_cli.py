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


def test_repl_evaluates_expression_then_exits_on_command():
    runner = CliRunner()
    result = runner.invoke(main, [], input="\\frac{1}{6} e^{5}\nexit\n")

    assert result.exit_code == 0
    assert math.isclose(
        _last_numeric_line(result.output), math.exp(5) / 6, rel_tol=1e-9
    )


def test_repl_exits_cleanly_on_eof():
    runner = CliRunner()
    result = runner.invoke(main, [], input="\\frac{1}{6} e^{5}\n")

    assert result.exit_code == 0
    assert "Traceback" not in result.output
    assert math.isclose(
        _last_numeric_line(result.output), math.exp(5) / 6, rel_tol=1e-9
    )


def test_repl_continues_after_bad_expression():
    runner = CliRunner()
    result = runner.invoke(
        main, [], input="\\frac{1}{\n\\frac{1}{6} e^{5}\nexit\n"
    )

    assert result.exit_code == 0
    assert "Error:" in result.output
    assert "Traceback" not in result.output
    assert math.isclose(
        _last_numeric_line(result.output), math.exp(5) / 6, rel_tol=1e-9
    )


def test_repl_continues_after_unbound_symbol():
    runner = CliRunner()
    result = runner.invoke(main, [], input="x + 1\n\\frac{1}{6} e^{5}\nexit\n")

    assert result.exit_code == 0
    assert "Error:" in result.output
    assert "Traceback" not in result.output
    assert math.isclose(
        _last_numeric_line(result.output), math.exp(5) / 6, rel_tol=1e-9
    )


def _last_numeric_line(output: str) -> float:
    for line in reversed(output.splitlines()):
        stripped = line.strip()
        if not stripped:
            continue
        try:
            return float(stripped.split()[-1])
        except ValueError:
            continue
    raise AssertionError(f"no numeric line found in output:\n{output!r}")
