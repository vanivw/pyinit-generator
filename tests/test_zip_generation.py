from pathlib import Path
import zipfile

from pyinit.generator import generate_project_zip


def test_generate_project_zip_creates_zip(tmp_path):
    zip_path = generate_project_zip(
        name="zip_app",
        stack="fastapi",
        pm="poetry",
        py="3.9",
        output_dir=tmp_path,
    )

    assert zip_path.exists()
    assert zip_path.suffix == ".zip"

    with zipfile.ZipFile(zip_path, "r") as zf:
        names = zf.namelist()

    assert "zip_app/pyproject.toml" in names
    assert "zip_app/README.md" in names