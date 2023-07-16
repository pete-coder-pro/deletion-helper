from pathlib import Path
from types import ModuleType
import click
import os
import glob


def delete_images(
    folder: Path, os_module: ModuleType = os, glob_module: ModuleType = glob
):
    """
    Delete all .png and .jpg files in a folder and its subfolders.

    Args:
        folder (str): The folder to delete the images from.
        os_module (ModuleType): The module to use for os operations.
        glob_module (ModuleType): The module to use for glob operations.

    Returns:
        int: The number of files deleted.
    """
    if os_module.path.isdir(str(folder)):
        files_deleted = 0
        for file_format in ["*.png", "*.jpg"]:
            pattern = str(Path(folder, "**", file_format))
            files = glob_module.glob(pattern, recursive=True)
            for file in files:
                os_module.remove(file)
                files_deleted += 1
        return files_deleted
    else:
        raise FileNotFoundError(f"The provided folder ({folder}) does not exist.")


@click.command()
@click.argument("folder", type=click.Path(exists=True))
def cli(folder: Path) -> None:
    """
    Delete all .png and .jpg files in a folder and its subfolders.

    Args:
        folder (Path): The folder to delete the images from.
    """
    try:
        deleted = delete_images(folder)
        click.echo(f"Deleted {deleted} .png and .jpg files in {folder}")
    except FileNotFoundError as e:
        click.echo(str(e))


if __name__ == "__main__":
    cli()
