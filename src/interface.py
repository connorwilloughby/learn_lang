"""Where we manage context passed to the cli, manages the game interface and acceptable views."""

import sys

from src.models.models import Question, TranslationResponse


class GameInterface:
    def __init__(
        self,
    ):
        self.menu_view = """\
    Press any key to begin the game

"""

        self.question_view = """\
    Translate: {question},

"""

        self.review_view = """\
    {user_answer} is {accuracy}.

    Other answers could have been {synonyms}

    Press any key to continue.

"""

    @staticmethod
    def _display(content: str):

        sys.stdout.write(content)
        sys.stdout.flush()

        return input(": ")

    def menu(
        self,
    ) -> None:
        """First screen used to route the user between the options available in the programme"""

        self._display(self.menu_view)

    def question(self, question: Question) -> str:
        """Sends the current question to the user"""

        question_screen = self.question_view.format(question=question.problem)

        return self._display(question_screen)

    def review(self, review: TranslationResponse):
        """We inform the user on the accuracy of their solution."""

        clean_synonyms = ", ".join(review.synonyms)

        return self._display(
            self.review_view.format(
                user_answer=review.user_solution,
                accuracy=review.accuracy,
                synonyms=clean_synonyms,
            )
        )


if __name__ == "__main__":
    GameInterface().menu()

    question_data = Question(problem="Casa", solution="House")

    stage = GameInterface().question(question_data)

    translation = TranslationResponse(
        accuracy=True, user_solution="house", synonyms=["home", "place"]
    )

    GameInterface().review(translation)
