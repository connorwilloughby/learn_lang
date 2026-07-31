"""Stores our test for the Tracking engine"""

import unittest
from unittest.mock import MagicMock, patch

from mocks.data import mock_all_stats_response, mock_stat

from interfaces.tracking import TrackingInterface
from models.question_types import QuestionStats


class TestTrackingEngine(unittest.TestCase):
    """Stores tests for the core Tracking engine"""

    def test_get_all_stats(self):
        """Assert that get_all_stats returns a sensible value"""
        # arrange
        mock_engine = MagicMock()
        mock_select = MagicMock(return_value=mock_all_stats_response)

        with patch("interfaces.local_db.sqlalchemy.create_engine", return_value=mock_engine) as _:
            tracking = TrackingInterface()

        tracking._select = mock_select

        # act
        stats = tracking.get_all_stats()

        # assert
        assert isinstance(stats, list)
        mock_select.assert_called()

    def test_get_problem_stats(self):
        """Assert that get_problem_stats returns a sensible value"""
        # arrange
        mock_engine = MagicMock()
        mock_select = MagicMock(return_value=mock_all_stats_response)

        with patch("interfaces.local_db.sqlalchemy.create_engine", return_value=mock_engine) as _:
            tracking = TrackingInterface()

        tracking._select = mock_select

        # act
        stats = tracking.get_problem_stats(1)

        # assert
        assert isinstance(stats, QuestionStats)
        assert stats.problem_id == mock_all_stats_response[0]["problem_id"]
        mock_select.assert_called()

    def test_clear_problems(self):
        """Assert that _clear_problems returns a sensible value"""
        # arrange
        mock_engine = MagicMock()
        mock_delete = MagicMock(return_value=1)

        with patch("interfaces.local_db.sqlalchemy.create_engine", return_value=mock_engine) as _:
            tracking = TrackingInterface()

        tracking._delete = mock_delete

        # act
        stats = tracking._clear_problems()

        # assert
        assert isinstance(stats, int)
        assert stats == 1
        mock_delete.assert_called()

    def test_check_problem_exists(self):
        """Assert that _check_problem returns a the existing val"""
        # arrange
        mock_engine = MagicMock()
        mock_select = MagicMock(return_value=mock_stat)

        with patch("interfaces.local_db.sqlalchemy.create_engine", return_value=mock_engine) as _:
            tracking = TrackingInterface()

        tracking._select = mock_select

        # act
        stats = tracking._check_problem(1)

        # assert
        assert isinstance(stats, bool)
        assert stats
        mock_select.assert_called()

    def test_check_problem_not_exists(self):
        """Assert that _check_problem returns False"""
        # arrange
        mock_engine = MagicMock()
        mock_select = MagicMock(return_value=[])

        with patch("interfaces.local_db.sqlalchemy.create_engine", return_value=mock_engine) as _:
            tracking = TrackingInterface()

        tracking._select = mock_select

        # act
        stats = tracking._check_problem(1)

        # assert
        assert isinstance(stats, bool)
        assert not stats
        mock_select.assert_called()

    def test_upsert_existing(self):
        """Assert that upsert_problem_stats returns False"""
        # arrange
        mock_engine = MagicMock()
        mock_select = MagicMock(return_value=mock_stat)
        mock_update = MagicMock(return_value=1)

        with patch("interfaces.local_db.sqlalchemy.create_engine", return_value=mock_engine) as _:
            tracking = TrackingInterface()

        tracking._select = mock_select
        tracking._update = mock_update

        # act
        stats = tracking.upsert_problem_stats(1, False)

        # assert
        assert isinstance(stats, bool)
        assert stats
        mock_select.assert_called()
        mock_update.assert_called()

    def test_upsert_new(self):
        """Assert that upsert_problem_stats returns False"""
        # arrange
        mock_engine = MagicMock()
        mock_select = MagicMock(return_value=[])
        mock_insert = MagicMock(return_value=mock_stat)

        with patch("interfaces.local_db.sqlalchemy.create_engine", return_value=mock_engine) as _:
            tracking = TrackingInterface()

        tracking._select = mock_select
        tracking._insert = mock_insert

        # act
        stats = tracking.upsert_problem_stats(1, False)

        # assert
        assert isinstance(stats, bool)
        assert stats
        mock_select.assert_called()
        mock_insert.assert_called()


if __name__ == "__main__":
    unittest.main()
