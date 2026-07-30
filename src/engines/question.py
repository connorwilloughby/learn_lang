from typing import Generator

import pandas as pd

from models.question_types import Question
from sources.sources import TargetSentences, TargetWords


class QuestionEngine:
    """Returns questions for the user to respond to."""

    # TODO: make this a param from the options menu
    def __init__(self, history=None, target: str = "sentences") -> None:

        if history:
            self._tracking_i = history

        if target == "words":
            self.questions: pd.DataFrame = TargetWords().load()
        elif target == "sentences":
            self.questions: pd.DataFrame = TargetSentences().load()
        else:
            raise ValueError("Unrecognized target param")

    def alternatives(self, problem_id: int) -> list[str]:
        """Return a list of alternative translations for a given problem id capped to 5 results

        :param problem_id: int: the problem id youre targeting.
        :rtype: list[str]
        """
        return list(self.questions[self.questions["id_es"] == problem_id]["sentence_en"])[:5]

    # TODO: will need promotion to engine eventually
    # TODO: probs needs some binning
    # TODO: support for randomization
    # TODO: support user init sort changes
    def sorting(self) -> pd.DataFrame:
        """Sort the frame based on the sorting algorithm"""
        questions = self.questions.copy()

        history = pd.DataFrame(self._tracking_i.get_all_stats())

        joined = questions.merge(
            history, how="left", left_on="id_es", right_on="problem_id"
        ).drop_duplicates("sentence_es")

        # count tokens sort
        joined["tokens"] = joined["sentence_es"].astype(str).str.split().apply(len)

        final = joined.sort_values(
            by=["last_n", "fail_count", "tokens"], ascending=[True, False, True]
        )

        return final

    def get_question(self) -> Generator[Question, Question, Question]:
        """Return a question from a given dataset."""
        sorting = self.sorting()

        for question in sorting.iterrows():
            data_row = question[1]
            yield Question(
                problem_id=data_row.id_es,
                problem=data_row.sentence_es,
                solution=data_row.sentence_en,
                alternatives=self.alternatives(data_row.id_es),
            )


if __name__ == "__main__":
    from interfaces.tracking import TrackingInterface

    questions = QuestionEngine(history=TrackingInterface(), target="sentences")

    this_question = questions.get_question()

    a = next(this_question)
    b = next(this_question)
    c = next(this_question)
    d = next(this_question)

    breakpoint()
