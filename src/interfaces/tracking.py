"""Module for holding tracking classes. These are responsible for tracking learning progress."""

# top level config
import logging

from config.config import ConfigWork
from interfaces.local_db import LocalDbInterface
from models.question_types import QuestionStats

CONFIG = ConfigWork()
PARENT_LOGGER = logging.getLogger(__name__)


class TrackingInterface(LocalDbInterface):
    """Manges all interactions with the local storage system"""

    def __init__(self):
        super().__init__()

    def _check_problem(self, problem_id: int):
        """Respond as true if the record exists in the db"""
        query = """SELECT
            *
        FROM 
            question_history
        WHERE
            problem_id == :problem_id
        """
        params = {"problem_id": problem_id}

        results = self._select(query=query, params=params)

        return results != []

    def _insert_problem(self, problem_id: int, correct: bool):
        """Insert row into problem table"""
        target_col = "correct_count" if correct else "fail_count"
        opposite_col = "correct_count" if not correct else "fail_count"

        query = f"""INSERT INTO
            question_history
            (problem_id, {target_col}, {opposite_col})
        VALUES 
            (:problem_id, 1, 0)
        RETURNING 
            tracking_id, problem_id
        """
        params = {"problem_id": problem_id}

        self._insert(query=query, params=params)

    def _update_problem(self, problem_id: int, correct: bool):
        """Update a given problem_id within the db

        :param problem_id: The id of the problem.
        :param correct: The status that you would like to record.
        """
        # used to infer the column based on outcome
        target_col = "correct_count" if correct else "fail_count"

        query = f"""UPDATE
            question_history
        SET
            {target_col} = {target_col} + 1 
        WHERE 
            problem_id = :problem_id
        RETURNING
            problem_id
        """

        params = {"problem_id": problem_id}

        self._update(query=query, params=params)

    def upsert_problem_stats(self, problem_id: int, correct: bool):
        """Upsert a given problem_id recording the outcomes"""
        exists = self._check_problem(problem_id=problem_id)

        if exists:
            self._update_problem(problem_id=problem_id, correct=correct)
        else:
            self._insert_problem(problem_id=problem_id, correct=correct)

        return True

    @staticmethod
    def _stats_handler(stats: list[dict]) -> QuestionStats | None:
        """Convert db response to pydantic model"""
        # we may not have asked this question prior
        if stats == []:
            return None

        return QuestionStats.model_validate(stats[0])

    def get_problem_stats(self, problem_id: int):
        """Get the statistics for a given problem from db"""
        query = """SELECT
            problem_id
            , correct_count
            , fail_count
            , correct_count + fail_count as attempts 
            , round(
                    cast(
                        correct_count AS REAL)
                             /
                        nullif(correct_count + fail_count, 0),
                    2
                ) AS pass_rate
        FROM 
            question_history
        WHERE
            problem_id == :problem_id
        """
        params = {"problem_id": problem_id}

        response_dict = self._select(query=query, params=params)

        return self._stats_handler(response_dict)

    def _clear_problems(
        self,
    ):

        query = """DELETE FROM question_history"""

        self._delete(query=query)

        return True


if __name__ == "__main__":
    track = TrackingInterface()

    flush = track._clear_problems()

    track.upsert_problem_stats(problem_id=1, correct=True)
    track.upsert_problem_stats(problem_id=1, correct=True)
    track.upsert_problem_stats(problem_id=1, correct=True)
    track.upsert_problem_stats(problem_id=2, correct=False)
    track.upsert_problem_stats(problem_id=2, correct=False)
    track.upsert_problem_stats(problem_id=2, correct=False)
    track.upsert_problem_stats(problem_id=2, correct=True)
    track.upsert_problem_stats(problem_id=2, correct=False)
    track.upsert_problem_stats(problem_id=3, correct=False)
    track.upsert_problem_stats(problem_id=3, correct=True)

    p1 = track.get_problem_stats(problem_id=1)
    p2 = track.get_problem_stats(problem_id=2)
    p3 = track.get_problem_stats(problem_id=3)

    breakpoint()
