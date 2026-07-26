from typing import Generator

import pandas as pd
from torch import Value

from models.question_types import Question
from sources.sources import TargetSentences, TargetWords


class QuestionEngine:
    """Returns questions for the user to respond to."""

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
        """Sort the frame based on the sorting algorithm"""
        questions = self.questions.copy()

        questions["sort_factor"] = questions["sentence_es"].astype(str).str.split().apply(len)

        return questions

    def get_question(self) -> Generator[Question, Question, Question]:
        """Return a question from a given dataset."""
        sorting = self.sorting()

        for question in sorting.sort_values("sort_factor", ascending=True).iterrows():
            data_row = question[1]
            yield Question(
                problem_id=data_row.id_es,
                problem=data_row.sentence_es,
                solution=data_row.sentence_en,
            )


if __name__ == "__main__":
    questions = QuestionEngine(target="sentences")

    this_question = questions.get_question()

    a = next(this_question)
    b = next(this_question)
    c = next(this_question)
    d = next(this_question)

    breakpoint()
