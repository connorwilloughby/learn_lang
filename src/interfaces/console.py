"""Where we manage context passed to the cli, manages the game interface and acceptable views."""

import sys

from models.question_types import Question, QuestionStats
from models.translation_types import TranslationResponse


class ConsoleInterface:
    """Update the STDOUT with information from the game engine"""

    def __init__(
        self,
    ):
        self.menu_view = """Press any key to begin the game
"""

        self.question_view = """    Attempts: {attempts} Success rate: {pass_rate}
    Themes: add_me
    Translate: {question}
"""

        self.review_view = """  {user_answer} is {accuracy}.

    We were expecting: {solution}

    Press any key to continue.
"""
    @staticmethod
    def _display(content: str):
        sys.stdout.write("\033[H\033[J")
        sys.stdout.write(content)
        sys.stdout.flush()

        return input("\t: ")

    def menu(
        self,
    ) -> None:
        """Show the first screen

        Used to route the user between the options available in the programme
        """
        self._display(self.menu_view)

    def question(self, question: Question, stats: QuestionStats | None) -> str:
        """Show a question to the user"""
        if stats is None:
            attempts = "0"
            pass_rate = "?"
        else:
            attempts = stats.attempts
            pass_rate = stats.pass_rate

        question_screen = self.question_view.format(
            question=question.problem, attempts=attempts, pass_rate=pass_rate
        )
        return self._display(question_screen)

    def review(self, review: TranslationResponse):
        """Show the user the accuracy of their solution"""
        clean_synonyms = ", ".join(review.synonyms)

        return self._display(
            self.review_view.format(
                user_answer=review.user_solution,
                accuracy=review.accuracy,
                solution=review.solution,
                synonyms=clean_synonyms,
            )
        )


if __name__ == "__main__":
    ConsoleInterface().menu()

    stats = QuestionStats(problem_id=1, correct_count=1, fail_count=1, pass_rate=0.5, attempts=2)

    question = Question(problem_id=1, problem="Casa", solution="House")

    stage = ConsoleInterface().question(question=question, stats=stats)

    translation = TranslationResponse(
        accuracy=True, user_solution="house", synonyms=["home", "place"]
    )

    ConsoleInterface().review(translation)
