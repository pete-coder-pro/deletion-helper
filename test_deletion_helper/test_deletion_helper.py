import os
from pathlib import Path
import random
import re
from typing import List
import pytest
from pytest_mock import MockerFixture
from deletion_helper.deletion_helper import delete_images


@pytest.fixture
def setup_files(tmp_path: Path):
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
    return files


def test_deletion_helper(setup_files: List[str], mocker: MockerFixture):
    """
    Test that deletion_helper deletes all .png and .jpg files in a folder
    and its subfolders.

    Args:
        setup_files (list): A list of files to be deleted.
        mocker (pytest_mock.plugin.MockerFixture): A pytest mocker fixture.
    """
    isdir_mock = mocker.patch("os.path.isdir")
    glob_mock = mocker.patch("glob.glob")
    remove_mock = mocker.patch("os.remove")

    isdir_mock.return_value = True

    # Fix the side effect to match the pattern correctly
    glob_mock.side_effect = lambda pattern, **kwargs: [
        f
        for f in setup_files
        if os.path.basename(f).endswith(tuple(pattern.split("/")[-1].split(".")[1:]))
    ]

    deletion_helper_calls = []
    remove_mock.side_effect = lambda x: deletion_helper_calls.append(x)

    expected_deletion_count = len(
        [f for f in setup_files if f.endswith(".png") or f.endswith(".jpg")]
    )

    folder = Path("/any/folder")
    delete_images(folder)

    assert len(deletion_helper_calls) == expected_deletion_count


def test_non_existing_folder(mocker):
    isdir_mock = mocker.patch("os.path.isdir")

    isdir_mock.return_value = False

    folder = Path("/non/existent/folder")
    with pytest.raises(
        FileNotFoundError,
        match=re.escape("The provided folder (/non/existent/folder) does not exist."),
    ):
        delete_images(folder)
