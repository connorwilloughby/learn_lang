"""Where we manage context passed to the cli, manages the game interface and acceptable views."""

import sys

from models.exception_types import GameMenuChange
from models.question_types import Question, QuestionStats
from models.translation_types import TranslationResponse
from utilities.text_utils import color_wrap


class ConsoleInterface:
    """Update the STDOUT with information from the game engine"""

    def __init__(
        self,
    ):

        self.shortcuts = """    -x: Return to Main Menu"""

        self.rc_mapping = "https://context.reverso.net/translation/spanish-english/"

        self.main_menu_view = """    Press any key to begin the game
"""

        self.menu_sort_view = """    Select a sort mode:
    {err}
        1: Learn new words
        2: Practice difficult words 
"""
        self.menu_mode_view = """    Select a game mode:
    {err}
        1: Sentences
        2: Words 
"""

        self.question_view = """    Attempts: {attempts} Success Rate: {pass_rate}
    Themes: add_me
    Translate: {question}
"""

        self.review_view = """    {user_answer} is {accuracy}.
    Translation: {problem} - {solution}
    Alternatives: {synonyms}

    Reverso Contexto: {link}

    Press any key to continue.
"""

    def _handle_user_changes(self, input: str):
        """"""
        if input == "-x":
            raise GameMenuChange

    def _display(self, content: str):
        sys.stdout.write("\033[H\033[J")
        sys.stdout.write(content)
        sys.stdout.flush()

        response = input("    : ")

        self._handle_user_changes(input=response)

        return response

    def menu_sort(self, misinput: bool = False):
        """"""

        val = "\n\tPrevious input cannot be parsed\n" if misinput else ""

        return self._display(self.menu_sort_view.format(err=color_wrap("red", val)))

    def menu_mode(self, misinput: bool = False):
        """"""

        val = "\n\tPrevious input cannot be parsed\n" if misinput else ""

        return self._display(self.menu_mode_view.format(err=color_wrap("red", val)))

    def question(self, question: Question, stats: QuestionStats | None) -> str:
        """Show a question to the user"""
        if stats is None:
            attempts = "0"
            pass_rate = "?"
        else:
            attempts = stats.attempts
            pass_rate = stats.pass_rate

        question_screen = self.question_view.format(
            question=color_wrap("blue", question.problem), attempts=attempts, pass_rate=pass_rate
        )
        return self._display(question_screen)

    def review(self, review: TranslationResponse):
        """Show the user the accuracy of their solution"""
        clean_synonyms = " ".join(review.alternatives)

        user_response = "--" if review.user_solution is None else review.user_solution

        translation = (
            color_wrap("green", "Correct") if review.accuracy else color_wrap("red", "Incorrect")
        )

        return self._display(
            self.review_view.format(
                user_answer=user_response,
                accuracy=translation,
                solution=color_wrap("white", review.solution),
                synonyms=color_wrap("blue", clean_synonyms),
                link=f"{self.rc_mapping}{review.problem}",
                problem=color_wrap("bright_magenta", review.problem),
            )
        )


if __name__ == "__main__":
    ConsoleInterface().menu_mode()

    stats = QuestionStats(problem_id=1, correct_count=1, fail_count=1, pass_rate=0.5, attempts=2)

    question = Question(problem_id=1, problem="Casa", solution="House")

    stage = ConsoleInterface().question(question=question, stats=stats)

    translation = TranslationResponse(
        accuracy=True,
        user_solution="house",
        problem=question.problem,
        alternatives=["home", "place"],
        solution="House",
    )

    ConsoleInterface().review(translation)
