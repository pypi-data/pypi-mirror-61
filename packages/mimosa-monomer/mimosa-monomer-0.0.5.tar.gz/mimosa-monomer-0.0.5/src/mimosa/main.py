import time
from enum import Enum

import typer
from halo import Halo

from . import sitekey

app = typer.Typer(no_args_is_help=True, help="The Awesome Stilt Admin CLI")
state = {"verbose": False}

app.add_typer(sitekey.app, name="sitekey")

existing_usernames = ["rick", "morty"]


class NeuralNetwork(Enum):
    simple = "simple"
    conv = "conv"
    lstm = "lstm"


@app.command(help="What's this?")
def neural(
    network: NeuralNetwork = typer.Option(
        NeuralNetwork.simple.value, case_sensitive=False
    ),
):
    spinner = Halo(text_color="yellow")
    spinner.start(f"Training a neural network of type: {network.value}")
    time.sleep(10)
    spinner.succeed()
    typer.secho("Was it worth it?", fg=typer.colors.BRIGHT_CYAN, bold=True)


@app.command()
def delete(
    force: bool = typer.Option(
        False,
        "--force",
        prompt="Are you sure you want to delete ALL the things?",
        help="Force deletion without confirmation",
    ),
):
    """A Test to delete all the things."""
    if force:
        typer.secho("EVERYTHING IS BEING DELETED", fg="red", bold=True)
    else:
        typer.secho("Ok, whew. That was close.", fg="bright_blue")


@app.callback()
def main_callback(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Not yet implemented."),
):
    if verbose:
        typer.echo("Verbose output enabled.")
        state["verbose"] = True


def main():
    app()


if __name__ == "__main__":
    main()
