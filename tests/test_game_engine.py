"""Stores our test for"""

import unittest
from unittest.mock import MagicMock, patch

import numpy as np

from engines.game import GameEngine


class TestGameEngine(unittest.TestCase):
    def setUp(self):
        self.engine = GameEngine()

    @patch("engines.game.CONFIG.TRANSLATION_PASSING_GRADE", np.float32(0.8))
    def test_translation_grade_pass(self):
        self.assertTrue(GameEngine._translation_grade(np.float32(0.8)))
        self.assertTrue(GameEngine._translation_grade(np.float32(0.9)))

    @patch("engines.game.CONFIG.TRANSLATION_PASSING_GRADE", np.float32(0.8))
    def test_translation_grade_fail(self):
        self.assertFalse(GameEngine._translation_grade(np.float32(0.79)))

    @patch("engines.game.ConsoleInterface")
    def test_handle_correct_answer(self, mock_console):
        question = MagicMock(
            problem_id=1,
            problem="hola",
            solution="hello",
        )

        self.engine.question_engine.get_question = MagicMock(return_value=iter([question]))

        self.engine.statistics.get_problem_stats = MagicMock(return_value={"x": 1})
        self.engine.translation_engine.translate = MagicMock(return_value=np.float32(0.95))
        self.engine.statistics.upsert_problem_stats = MagicMock()
        self.engine.interface.review = MagicMock()

        mock_console.return_value.question.return_value = "hello"

        with self.assertRaises(StopIteration):
            self.engine.handle()

        mock_console.return_value.menu.assert_called_once()
        mock_console.return_value.question.assert_called_once_with(
            question=question,
            stats={"x": 1},
        )
        self.engine.translation_engine.translate.assert_called_once_with("hello", "hola")
        self.engine.statistics.upsert_problem_stats.assert_called_once_with(
            problem_id=1,
            correct=True,
        )
        self.engine.interface.review.assert_called_once()

    @patch("engines.game.ConsoleInterface")
    def test_handle_incorrect_answer(self, mock_console):
        question = MagicMock(
            problem_id=5,
            problem="bonjour",
            solution="hello",
        )

        self.engine.question_engine.get_question = MagicMock(return_value=iter([question]))

        self.engine.statistics.get_problem_stats = MagicMock(return_value={})
        self.engine.translation_engine.translate = MagicMock(return_value=np.float32(0.1))
        self.engine.statistics.upsert_problem_stats = MagicMock()
        self.engine.interface.review = MagicMock()

        mock_console.return_value.question.return_value = "bye"

        with self.assertRaises(StopIteration):
            self.engine.handle()

        self.engine.statistics.upsert_problem_stats.assert_called_once_with(
            problem_id=5,
            correct=False,
        )

        review = self.engine.interface.review.call_args.args[0]
        self.assertEqual(review.user_solution, "bye")
        self.assertEqual(review.solution, "hello")
        self.assertEqual(review.accuracy, np.float32(0.1).T)


if __name__ == "__main__":
    unittest.main()
