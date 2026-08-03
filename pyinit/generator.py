from pathlib import Path
import os
import tempfile
import shutil

from jinja2 import Environment, FileSystemLoader, StrictUndefined


TEMPLATES_DIR = Path(__file__).parent / "templates"

VALID_STACKS = {"lib", "fastapi", "cli"}
VALID_PACKAGE_MANAGERS = {"poetry", "hatch", "pdm"}


def render_tree(env: Environment, src_dir: Path, dst_dir: Path, context: dict):
    for root, dirs, files in os.walk(src_dir):
        rel = Path(root).relative_to(src_dir)

        rendered_rel = Path(env.from_string(str(rel)).render(**context))

        out_dir = dst_dir / rendered_rel
        out_dir.mkdir(parents=True, exist_ok=True)

        for f in files:
            src_path = Path(root) / f

            rendered_name = env.from_string(f).render(**context)
            rendered_name = rendered_name.replace(".j2", "")

            with open(src_path, "r", encoding="utf-8") as fh:
                tpl = env.from_string(fh.read())

            (out_dir / rendered_name).write_text(
                tpl.render(**context),
                encoding="utf-8"
            )


def generate_project(
    name: str,
    stack: str = "lib",
    pm: str = "poetry",
    py: str = "3.12",
    ci: str = "github",
    docker: bool = False,
    output_dir: Path | None = None,
) -> Path:
    stack = stack.lower()
    pm = pm.lower()

    if stack not in VALID_STACKS:
        raise ValueError("stack must be one of: lib, fastapi, cli")

    if pm not in VALID_PACKAGE_MANAGERS:
        raise ValueError("pm must be one of: poetry, hatch, pdm")

    base_dir = output_dir or Path.cwd()
    project_dir = base_dir / name

    if project_dir.exists():
        raise FileExistsError(f"Directory '{name}' already exists")

    context = {
        "project_name": name,
        "package_name": name.replace("-", "_"),
        "stack": stack,
        "package_manager": pm,
        "python_version": py,
        "ci": ci,
        "docker": docker,
        "use_precommit": True,
        "use_mypy": True,
        "use_ruff": True,
        "license": "MIT",
    }

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        undefined=StrictUndefined,
        keep_trailing_newline=True,
        autoescape=False,
        lstrip_blocks=True,
        trim_blocks=True,
    )

    project_dir.mkdir(parents=True, exist_ok=False)

    render_tree(env, TEMPLATES_DIR / "base", project_dir, context)
    render_tree(env, TEMPLATES_DIR / stack, project_dir, context)

    return project_dir

def generate_project_zip(
    name: str,
    stack: str = "lib",
    pm: str = "poetry",
    py: str = "3.12",
    ci: str = "github",
    docker: bool = False,
    output_dir: Path | None = None,
) -> Path:
    """
    Generate a project in a temporary folder and return a zip file path.
    This will be used by the Web UI later.
    """
    base_output_dir = output_dir or Path.cwd()

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        project_path = generate_project(
            name=name,
            stack=stack,
            pm=pm,
            py=py,
            ci=ci,
            docker=docker,
            output_dir=temp_path,
        )

        zip_base_path = base_output_dir / name
        zip_path = shutil.make_archive(
            base_name=str(zip_base_path),
            format="zip",
            root_dir=project_path.parent,
            base_dir=project_path.name,
        )

        return Path(zip_path)