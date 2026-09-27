from pathlib import Path
import socket
import subprocess
import sys
import venv

import typer


def venv_python_path(venv_dir: Path) -> Path:
    if sys.platform == "win32":
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


def create_venv(project_dir: Path) -> Path:
    venv_dir = project_dir / ".venv"
    venv.EnvBuilder(with_pip=True, clear=True).create(venv_dir)
    return venv_dir


def install_project(project_dir: Path, venv_python: Path) -> None:
    subprocess.run(
        [str(venv_python), "-m", "pip", "install", "."],
        cwd=project_dir,
        check=True,
    )


def launch_project(project_dir: Path, venv_python: Path, stack: str, package_name: str) -> None:
    if stack == "fastapi":
        subprocess.run(
            [str(venv_python), "-m", "uvicorn", f"{package_name}.main:app", "--reload"],
            cwd=project_dir,
            check=True,
        )
    elif stack == "cli":
        subprocess.run(
            [str(venv_python), "-m", package_name],
            cwd=project_dir,
            check=True,
        )
    # lib: nothing to launch


def run_project(project_dir: Path, stack: str, package_name: str) -> None:
    typer.echo("Creating virtual environment (.venv)...")
    venv_dir = create_venv(project_dir)
    py = venv_python_path(venv_dir)

    typer.echo("Installing project dependencies...")
    install_project(project_dir, py)

    if stack == "lib":
        typer.secho(
            "Installed into .venv -- libraries have no entrypoint to launch.",
            fg=typer.colors.GREEN,
        )
        return

    if stack == "fastapi":
        typer.echo("Launching dev server (Ctrl+C to stop)...")
    else:
        typer.echo("Launching project...")

    launch_project(project_dir, py, stack, package_name)


def find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def launch_fastapi_background(
    project_dir: Path, venv_python: Path, package_name: str, port: int
) -> subprocess.Popen:
    return subprocess.Popen(
        [
            str(venv_python), "-m", "uvicorn",
            f"{package_name}.main:app",
            "--host", "127.0.0.1",
            "--port", str(port),
        ],
        cwd=project_dir,
    )
