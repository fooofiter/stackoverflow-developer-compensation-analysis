"""Download and verify the official 2025 Stack Overflow survey files."""

from __future__ import annotations

import argparse
import hashlib
import shutil
from pathlib import Path
from urllib.request import Request, urlopen


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
BASE_URL = (
    "https://github.com/StackExchange/Survey/raw/refs/heads/main/"
    "packages/archive/2025"
)
FILES = {
    "results.csv": {
        "sha256": (
            "2d1f65308877282edfb4470520eabbc08cb499118432a3dcec6a66c086aa2baa"
        ),
    },
    "schema.csv": {
        "sha256": (
            "1d24951e04eab46c6f9fecef6ce8e6b32a0a14a3f0eecdcf62f70833a74b3ff8"
        ),
    },
}


def sha256(path: Path) -> str:
    """Return the SHA-256 digest of a file."""
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def download_file(url: str, destination: Path) -> None:
    """Download a URL to a temporary file, then move it into place."""
    temporary = destination.with_suffix(destination.suffix + ".part")
    request = Request(url, headers={"User-Agent": "udacity-ds-blog-project"})
    with urlopen(request) as response, temporary.open("wb") as output:
        shutil.copyfileobj(response, output)
    temporary.replace(destination)


def main() -> None:
    """Download missing files and verify all expected hashes."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--force",
        action="store_true",
        help="Download files again even when verified local copies exist.",
    )
    args = parser.parse_args()
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    for filename, metadata in FILES.items():
        destination = RAW_DATA_DIR / filename
        expected_hash = metadata["sha256"]

        if destination.exists() and not args.force:
            if sha256(destination) == expected_hash:
                print(f"Verified existing file: {destination}")
                continue
            raise RuntimeError(
                f"Hash mismatch for {destination}. Remove it or use --force."
            )

        print(f"Downloading {filename}...")
        download_file(f"{BASE_URL}/{filename}", destination)
        actual_hash = sha256(destination)
        if actual_hash != expected_hash:
            destination.unlink(missing_ok=True)
            raise RuntimeError(
                f"Hash mismatch for {filename}: expected {expected_hash}, "
                f"received {actual_hash}."
            )
        print(f"Downloaded and verified: {destination}")


if __name__ == "__main__":
    main()
