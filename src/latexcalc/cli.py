import readline  # noqa: F401  (enables arrow-key line editing in REPL)
import sys

import click

from latexcalc.evaluator import evaluate


@click.command()
@click.argument("expression", required=False)
def main(expression: str | None) -> None:
    if expression is None:
        run_repl()
        return
    try:
        result = evaluate(expression)
    except ValueError as exc:
        click.echo(f"Error: {exc}")
        sys.exit(1)
    click.echo(result)


def run_repl() -> None:
    while True:
        try:
            line = input("latexcalc> ")
        except EOFError:
            click.echo()
            return
        if line.strip() == "exit":
            return
        try:
            click.echo(evaluate(line))
        except ValueError as exc:
            click.echo(f"Error: {exc}")
