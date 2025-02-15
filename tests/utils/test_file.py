import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from utils.file import copy_file, file_exists


@pytest.fixture
def temp_dirs_with_files():
    with tempfile.TemporaryDirectory() as src_dir, tempfile.TemporaryDirectory() as dest_dir:
        # create sample files
        with open(os.path.join(src_dir, "sample1.mp3"), "w") as file:
            file.write("Test file 1")

        with open(os.path.join(src_dir, "sample2.mp3"), "w") as file:
            file.write("Test file 2")

        with open(os.path.join(dest_dir, "sample2.mp3"), "w") as file:
            file.write("Test file 2")

        yield src_dir, dest_dir


def test_file_exists_should_return_true_when_file_exists(temp_dirs_with_files):
    src_dir, dest_dir = temp_dirs_with_files
    with patch("utils.file.DEFAULT_AUDIO_KEEPER", Path(dest_dir)):
        assert file_exists(Path(src_dir) / "sample2.mp3")


def test_file_exists_should_return_false_when_file_does_not_exists(
    temp_dirs_with_files,
):
    src_dir, dest_dir = temp_dirs_with_files
    with patch("utils.file.DEFAULT_AUDIO_KEEPER", Path(dest_dir)):
        assert not file_exists(Path(src_dir) / "sample1.mp3")


def test_copy_file_should_copy_file_if_file_does_not_exists_in_destination(
    temp_dirs_with_files,
):
    """Ensure that function work properly. Should return path and in the destination directory should be new file."""
    src_dir, dest_dir = temp_dirs_with_files
    copy_file_name = "sample1.mp3"
    assert not os.path.exists(Path(dest_dir) / copy_file_name)
    _path = copy_file(Path(src_dir) / copy_file_name, to=Path(dest_dir))
    assert isinstance(_path, Path)
    expected_path = Path(dest_dir) / copy_file_name
    assert _path == expected_path
    assert os.path.exists(expected_path)


def test_copy_file_should_not_copy_file_if_file_exists_in_destination(
    temp_dirs_with_files,
):
    src_dir, dest_dir = [Path(p) for p in temp_dirs_with_files]
    copy_file_name = Path("sample2.mp3")
    with patch("utils.file.DEFAULT_AUDIO_KEEPER", dest_dir):
        assert os.path.exists(dest_dir / copy_file_name)
        assert not copy_file(src_dir / copy_file_name, to=dest_dir)
