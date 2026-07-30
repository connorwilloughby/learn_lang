import numpy as np

from config.config import ConfigWork
from engines.question import QuestionEngine
from engines.translator import Translator
from interfaces.console import ConsoleInterface
from interfaces.tracking import TrackingInterface
from models.translation_types import TranslationResponse
from utilities.text_utils import color_wrap

CONFIG = ConfigWork()


class GameEngine:
    """Instructs all child classes and orchestrates the game"""

    def __init__(self) -> None:

        self.question_engine = QuestionEngine()
        self.translation_engine = Translator()
        self.statistics = TrackingInterface()
        self.interface = ConsoleInterface()

    @staticmethod
    def _translation_grade(score: np.float32) -> bool:
        """Evaluate if a given score should be considered as a pass

        Params:
            :param score np.float32
        """
        return bool(score >= CONFIG.TRANSLATION_PASSING_GRADE)

    def handle(self):
        """Manage the main gameplay loop"""
        ConsoleInterface().menu()

        # allow the iterator to persist across questions
        question_state = self.question_engine.get_question()

        while True:
            # prepare a question
            question = next(question_state)
            stats = self.statistics.get_problem_stats(problem_id=question.problem_id)

            # ask a question
            user_response = ConsoleInterface().question(question=question, stats=stats)

            # score the translation
            score = self.translation_engine.translate(user_response, question.problem)

            # TODO: tell the user if it was right...
            # convert the score to bool
            accurate_translation = self._translation_grade(score)

            # record this result
            self.statistics.upsert_problem_stats(
                problem_id=question.problem_id, correct=accurate_translation
            )

            #  review the attempt
            self.interface.review(
                TranslationResponse(
                    accuracy=color_wrap("green", "Correct")
                    if accurate_translation
                    else color_wrap("red", "Incorrect"),
                    user_solution=user_response,
                    solution=question.solution,
                )
            )
