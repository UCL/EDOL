import typer

app = typer.Typer()


@app.command()
def serl(ctx: typer.Context) -> None:
    """
    Generate SERL report.
    """
    typer.echo(ctx.obj)
    typer.echo("Climate commands.")
    typer.echo("Not implemented yet.")
    raise typer.Exit(1)
