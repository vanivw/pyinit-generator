from typer.testing import CliRunner
from pyinit.cli import app
from pathlib import Path

runner = CliRunner()

def test_invalid_stack_fails():
    result = runner.invoke(app, ["bad_app", "--stack", "invalid"])
    assert result.exit_code != 0
    assert "stack must be one of" in (result.stdout + result.stderr)

def test_invalid_pm_fails():
    result = runner.invoke(app, ["bad_app", "--pm", "pipenv"])
    assert result.exit_code != 0
    assert "pm must be one of" in (result.stdout + result.stderr)

def test_existing_directory_fails_isolated():
    with runner.isolated_filesystem():
        Path("my_app").mkdir()
        result = runner.invoke(app, ["my_app"])
        assert result.exit_code != 0
        assert "already exists" in result.stdout

