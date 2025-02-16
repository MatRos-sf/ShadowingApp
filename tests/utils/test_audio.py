from pathlib import Path

import pytest

from models.session_manager import AudioSession
from utils.audio import TimeStampManager


@pytest.fixture
def sample_audio_session():
    return AudioSession(1, "Session 1", Path("/old/path"), [1.0, 2.0], 120, 30, 5)


class TestTimeStampManager:
    @pytest.mark.parametrize(
        "audio_session, expected",
        [
            (
                AudioSession(1, "Session 1", Path("/old/path"), [0.1, 0.2], 120, 30, 5),
                0.2,
            ),
            (AudioSession(1, "Session 1", Path("/old/path"), [], 120, 30, 5), 0),
        ],
    )
    def test_should_return_current_stamp(self, audio_session, expected):
        time_stamp_instance = TimeStampManager(audio_session)
        assert time_stamp_instance.stamp == expected

    @pytest.mark.parametrize(
        "audio_session, expected",
        [
            (
                AudioSession(1, "Session 1", Path("/old/path"), [0.1, 0.2], 120, 30, 5),
                [0.1, 0.2],
            ),
            (AudioSession(1, "Session 1", Path("/old/path"), [], 120, 30, 5), [0]),
        ],
    )
    def test_should_return_time_stamp_list(self, audio_session, expected):
        time_stamp_instance = TimeStampManager(audio_session)
        assert time_stamp_instance.time_stamp_list == expected

    @pytest.mark.parametrize("value", [1, 3, 10])
    def test_should_not_set_new_time_stamp_index_when_value_is_bigest_than_list(
        self, value, sample_audio_session
    ):
        instance = TimeStampManager(sample_audio_session)
        index = instance.time_stamp_index
        instance.time_stamp_index += value
        assert index == instance.time_stamp_index

    def test_should_add_new_time_stamp(self, sample_audio_session):
        instance = TimeStampManager(sample_audio_session)
        initial_length = len(instance.time_stamp_list)
        new_time_stamp = 3.0
        result = instance.add_time_stamp(new_time_stamp)
        assert result is True
        assert len(instance.time_stamp_list) == initial_length + 1
        assert new_time_stamp in instance.time_stamp_list

    def test_should_not_add_duplicate_time_stamp(self, sample_audio_session):
        instance = TimeStampManager(sample_audio_session)
        initial_length = len(instance.time_stamp_list)
        duplicate_time_stamp = 2
        result = instance.add_time_stamp(duplicate_time_stamp)
        assert result is False
        assert len(instance.time_stamp_list) == initial_length

    @pytest.mark.parametrize(
        "index, expected_range", [(0, (1.0, 2.0)), (1, (2.0, None))]
    )
    def test_should_return_correct_range(
        self, sample_audio_session, index, expected_range
    ):
        instance = TimeStampManager(sample_audio_session)
        instance.time_stamp_index = index
        assert instance.range() == expected_range
