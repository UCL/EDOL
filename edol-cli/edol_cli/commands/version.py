import toml
import typer

app = typer.Typer()


@app.callback(invoke_without_command=True)
def version() -> None:
    # read from pyproject.toml
    pyproject = toml.load("pyproject.toml")
    name = pyproject["tool"]["poetry"]["name"]
    version = pyproject["tool"]["poetry"]["version"]

    typer.echo(f"{name} version {version}")
