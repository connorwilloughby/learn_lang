from typing import Generator

import pandas as pd

from src.sources.sources import TargetSentences, TargetWords
from src.models.models import Question


class QuestionEngine:
    """Returns questions for the user to respond to.

    Is the core gameplay loop."""

    def __init__(self, target: str = "sentences") -> None:

        if target == "words":
            self.questions: pd.DataFrame = TargetWords().load()
        elif target == "sentences":
            self.questions: pd.DataFrame = TargetSentences().load()

    def get_question(self) -> Generator[Question]:
        """Returns a question from a given dataset."""

        for question in self.questions.iterrows():
            data_row = question[1]
            yield Question(problem=data_row.sentence_es, solution=data_row.sentence_en)


if __name__ == "__main__":
    questions = QuestionEngine(target="words")

    this_question = questions.get_question()

    a = next(this_question)
    b = next(this_question)

    breakpoint()
