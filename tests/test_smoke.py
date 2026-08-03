import os
import subprocess
import sys
from pathlib import Path


def run_pyinit(tmp_path: Path):
    # Run "pyinit" as a module to ensure we're testing THIS source tree
    cmd = [
        sys.executable,
        "-m",
        "pyinit.cli",
        "smoke_app",
        "--stack",
        "lib",
        "--pm",
        "poetry",
        "--py",
        "3.9",
    ]
    subprocess.run(cmd, cwd=tmp_path, check=True)


def test_generator_creates_project(tmp_path: Path):
    run_pyinit(tmp_path)

    out = tmp_path / "smoke_app"
    assert out.exists()
    assert (out / "pyproject.toml").exists()
    assert (out / "README.md").exists()


def test_no_unrendered_jinja_tokens(tmp_path: Path):
    run_pyinit(tmp_path)

    out = tmp_path / "smoke_app"
    # Scan all generated text files for leftover template variables like {{ ... }}
    for p in out.rglob("*"):
        if p.is_file() and p.suffix in {".py", ".toml", ".md", ".yml", ".yaml", ".txt"}:
            text = p.read_text(encoding="utf-8", errors="ignore")
            assert "{{" not in text and "}}" not in text, f"Found Jinja token in {p}"
