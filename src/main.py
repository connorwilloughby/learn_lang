import numpy as np

from src.config.config import ConfigWork
from src.engines.questions import QuestionEngine
from src.engines.translate import Translator
from src.interface import GameInterface
from src.models.models import TranslationResponse


class GameManager:
    """Instructs all child classes and orchestrates the game"""

    def __init__(self) -> None:

        self.question_engine = QuestionEngine().get_question()

        self.translation_engine = Translator()

    @staticmethod
    def _translation_grade(score: np.float32) -> bool:

        return score >= ConfigWork.TRANSLATION_PASSING_GRADE

    def handle(self):
        """Manage the main gameplay loop"""
        GameInterface().menu()

        while True:
            # prepare a question
            question = next(self.question_engine)

            # ask a question
            user_response = GameInterface().question(question)

            # score the translation
            score = self.translation_engine.translate(user_response, question.problem)

            # convert the score to bool
            correct_translation = self._translation_grade(score)

            #  review the attempt
            GameInterface().review(
                TranslationResponse(
                    accuracy=score.T,
                    user_solution=user_response,
                    solution=question.solution,
                )
            )


if __name__ == "__main__":
    GameManager().handle()
