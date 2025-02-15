import shutil
from pathlib import Path
from typing import Optional

DEFAULT_AUDIO_KEEPER = Path(__file__).parent.parent / Path("audio")


def file_exists(file_path: Path) -> bool:
    file_name = file_path.name
    return Path(DEFAULT_AUDIO_KEEPER / file_name).is_file()


def copy_file(
    file_path: Path, to: Path = DEFAULT_AUDIO_KEEPER, new_name: Optional[str] = None
) -> Optional[Path]:
    """
    Copies a file to the specified directory if it doesn't already exists there.
    Optionally renames the file during the copy.

    Returns:
        Optional[Path]: The path to the copied file, or None if the file already exists.
    """
    if not file_exists(file_path):
        destination = to / (new_name + file_path.name if new_name else file_path.name)
        return Path(shutil.copy(file_path, destination))
    return
