"""Execute the final project notebook and save a clean public copy."""

from __future__ import annotations

from pathlib import Path

import nbformat as nbf
from nbclient import NotebookClient


PROJECT_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = (
    PROJECT_ROOT
    / "notebooks"
    / "stackoverflow_developer_compensation.ipynb"
)


def remove_stderr_outputs(notebook: nbf.NotebookNode) -> None:
    """Remove environment-specific warning streams from executed cells."""
    for cell in notebook.cells:
        if cell.cell_type != "code":
            continue
        cell.outputs = [
            output
            for output in cell.get("outputs", [])
            if not (
                output.get("output_type") == "stream"
                and output.get("name") == "stderr"
            )
        ]


def main() -> None:
    """Run the tracked notebook from a clean kernel and save its outputs."""
    notebook = nbf.read(NOTEBOOK_PATH, as_version=4)
    for cell in notebook.cells:
        if cell.cell_type == "code":
            cell.execution_count = None
            cell.outputs = []

    client = NotebookClient(
        notebook,
        timeout=3600,
        kernel_name="python3",
        resources={"metadata": {"path": str(PROJECT_ROOT)}},
    )
    client.execute()
    remove_stderr_outputs(notebook)
    nbf.write(notebook, NOTEBOOK_PATH)
    print(f"Executed and saved {NOTEBOOK_PATH}")


if __name__ == "__main__":
    main()
