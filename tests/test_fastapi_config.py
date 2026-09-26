import importlib.util

from pyinit.generator import generate_project


def test_fastapi_template_includes_pyyaml_dependency(tmp_path):
    project_dir = generate_project(
        name="config_app",
        stack="fastapi",
        pm="poetry",
        py="3.9",
        output_dir=tmp_path,
    )

    pyproject_text = (project_dir / "pyproject.toml").read_text(encoding="utf-8")
    assert "pyyaml" in pyproject_text.lower()


def test_fastapi_template_generates_config_files(tmp_path):
    project_dir = generate_project(
        name="config_app",
        stack="fastapi",
        pm="poetry",
        py="3.9",
        output_dir=tmp_path,
    )

    assert (project_dir / "config.yaml").exists()
    assert (project_dir / "config_app" / "config.py").exists()


def test_generated_config_loads_correctly(tmp_path):
    project_dir = generate_project(
        name="config_app",
        stack="fastapi",
        pm="poetry",
        py="3.9",
        output_dir=tmp_path,
    )

    config_module_path = project_dir / "config_app" / "config.py"
    spec = importlib.util.spec_from_file_location("config_app_config", config_module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    assert module.settings["app"]["name"] == "config_app"
    assert module.settings["server"]["port"] == 8000