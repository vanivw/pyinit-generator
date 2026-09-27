import subprocess

import typer

from pyinit.generator import generate_project
from pyinit.runner import run_project


app = typer.Typer(
    help="PyInit - Minimal Python project generator",
    no_args_is_help=True,
)


@app.command()
def main(
    name: str = typer.Argument(..., help="Project name (folder will be created)"),
    stack: str = typer.Option("lib", "--stack", "-s", help="Type of project"),
    pm: str = typer.Option("poetry", "--pm", help="Package manager (poetry/hatch/pdm)"),
    py: str = typer.Option("3.12", "--py", help="Target Python version for generated project"),
    ci: str = typer.Option("github", "--ci", help="CI provider (none/github)"),
    docker: bool = typer.Option(False, "--docker", help="Include Dockerfile"),
    run: bool = typer.Option(
        False, "--run", help="Create a venv, install, and launch the generated project"
    ),
):
    try:
        project_dir = generate_project(
            name=name,
            stack=stack,
            pm=pm,
            py=py,
            ci=ci,
            docker=docker,
        )
    except ValueError as e:
        raise typer.BadParameter(str(e))
    except FileExistsError as e:
        typer.secho(f"✖ {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    typer.secho(f"✔ Created {name}", fg=typer.colors.GREEN)

    if run:
        package_name = name.replace("-", "_")
        try:
            run_project(project_dir, stack, package_name)
        except subprocess.CalledProcessError as e:
            typer.secho(f"✖ --run failed: {e}", fg=typer.colors.RED)
            raise typer.Exit(code=1)
        return

    typer.echo("Next steps:")
    typer.echo(f"  cd {name}")

    if pm == "poetry":
        typer.echo("  poetry install && poetry run pytest -q")
    elif pm == "hatch":
        typer.echo("  hatch env create && hatch run test")
    else:
        typer.echo("  pdm install && pdm run pytest -q")


if __name__ == "__main__":
    app()