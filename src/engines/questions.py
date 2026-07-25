from typing import Generator

import pandas as pd
from torch import Value

from src.sources.sources import TargetSentences, TargetWords
from src.types.models import Question


class QuestionEngine:
    """Returns questions for the user to respond to.

    Is the core gameplay loop.
    """

    # TODO: make this a param from the options menu
    def __init__(self, target: str = "sentences") -> None:

        if target == "words":
            self.questions: pd.DataFrame = TargetWords().load()
        elif target == "sentences":
            self.questions: pd.DataFrame = TargetSentences().load()
        else:
            raise Value("Unrecognized target param")

    # TODO: probs needs some binning
    def sorting(self) -> pd.DataFrame:
        """"""
        questions = self.questions.copy()

        questions["sort_factor"] = (
            questions["sentence_es"].astype(str).str.split().apply(len)
        )

        return questions

    def get_question(self) -> Generator[Question, Question, Question]:
        """Return a question from a given dataset."""
        sorting = self.sorting()

        for question in sorting.sort_values("sort_factor", ascending=True).iterrows():
            data_row = question[1]
            yield Question(problem=data_row.sentence_es, solution=data_row.sentence_en)


if __name__ == "__main__":
    questions = QuestionEngine(target="sentences")

    this_question = questions.get_question()

    a = next(this_question)
    b = next(this_question)

    breakpoint()
