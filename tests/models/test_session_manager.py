from pathlib import Path

import pytest

from models.session_manager import AudioSession


@pytest.mark.parametrize(
    "audio_session, audio_session_other, excpected",
    [
        (
            AudioSession(1, "Session 1", Path("/old/path"), [0.1, 0.2], 120, 30, 5),
            AudioSession(
                1, "Session 1", Path("/new/path"), [0.1, 0.2, 0.3], 120, 35, 5
            ),
            {"file_path": "/new/path", "time_stamp": "0.1,0.2,0.3", "spend_time": 35},
        )
    ],
)
def test_diff_should_return_dict_with_diffrent(
    audio_session, audio_session_other, excpected
):
    diff = audio_session.diff(audio_session_other)
    assert diff == excpected
