from pathlib import Path
import random
import re
import pytest
from deletion_helper.deletion_helper import delete_images


@pytest.fixture
def test_folder(tmp_path: Path):
    """
    Create 20 files with random extensions in a temporary directory.

    Args:
        tmp_path (Path)f: A temporary directory.
    """
    extensions = ["png", "jpg", "txt", "doc", "mp3"]
    files = []
    for _ in range(20):
        ext = extensions[random.randint(0, len(extensions) - 1)]
        filepath = tmp_path / f"tempfile.{ext}"
        with open(filepath, "w") as f:
            f.write("content")
        files.append(str(f))
    return tmp_path


def test_deletion_helper(test_folder: Path) -> None:
    """
    Test that deletion_helper deletes all .png and .jpg files in a folder
    and its subfolders.

    Args:
        test_folder (Path): The temporary directory with the test files.
    """

    # Create a list of files to be deleted
    images_count = 0
    for f in test_folder.glob("**/*"):
        if f.suffix == ".png" or f.suffix == ".jpg":
            images_count += 1

    deleted_images_count = delete_images(test_folder)

    assert images_count == deleted_images_count


def test_non_existing_folder() -> None:
    """
    Test that deletion_helper raises a FileNotFoundError if the provided
    folder does not exist.
    """
    folder = Path("/non/existent/folder")
    with pytest.raises(
        FileNotFoundError,
        match=re.escape("The provided folder (/non/existent/folder) does not exist."),
    ):
        delete_images(folder)
