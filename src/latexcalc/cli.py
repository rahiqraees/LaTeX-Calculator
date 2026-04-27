import sys

import click

from latexcalc.evaluator import evaluate


@click.command()
@click.argument("expression")
def main(expression: str) -> None:
    try:
        result = evaluate(expression)
    except ValueError as exc:
        click.echo(f"Error: {exc}", err=False)
        sys.exit(1)
    click.echo(result)
