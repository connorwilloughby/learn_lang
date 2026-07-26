import numpy as np

from src.config.config import ConfigWork
from src.engines.questions import QuestionEngine
from src.engines.tracking import Tracker
from src.engines.translate import Translator
from src.interface import GameInterface
from src.types.models import TranslationResponse

CONFIG = ConfigWork()

class GameManager:
    """Instructs all child classes and orchestrates the game"""

    def __init__(self) -> None:

        self.question_engine = QuestionEngine()
        self.translation_engine = Translator()
        self.statistics = Tracker()
        self.interface = GameInterface()

    @staticmethod
    def _translation_grade(score: np.float32) -> bool:
        """Evaluate if a given score should be considered as a pass 

        Params:
            :param score np.float32
        """

        return bool(score >= CONFIG.TRANSLATION_PASSING_GRADE)

    def handle(self):
        """Manage the main gameplay loop"""
        GameInterface().menu()

        while True:
            # prepare a question
            question = next(self.question_engine.get_question())
            stats = self.statistics.get_problem_stats(problem_id=question.problem_id)

            # ask a question
            user_response = GameInterface().question(question=question, stats=stats)

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
                    accuracy=score.T,
                    user_solution=user_response,
                    solution=question.solution,
                )
            )


if __name__ == "__main__":
    GameManager().handle()
