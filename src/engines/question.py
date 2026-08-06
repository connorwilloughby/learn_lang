from typing import Generator

import pandas as pd

from models.question_types import Question
from models.game_types import SortingTypes
from sources.sources import TargetSentences, TargetWords

STYPES = SortingTypes()


class QuestionEngine:
    """Returns questions for the user to respond to."""

    # TODO: make this a param from the options menu
    def __init__(self, sorting: int = None, history=None, game_mode: str = "sentences") -> None:

        if history:
            self._tracking_i = history

        self.sorting_mode: int = sorting

        # setup the class
        self._handle_game_modes(target=game_mode)

    def _handle_game_modes(self, target: str):
        """"""
        if target == "words":
            self.questions = TargetWords().load()
        elif target == "sentences":
            self.questions = TargetSentences().load()
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
    def sorting(self, revision_mode: bool = True) -> pd.DataFrame:
        """Sort the frame based on the sorting algorithm"""
        questions = self.questions.copy()

        history = pd.DataFrame(self._tracking_i.get_all_stats())

        joined = questions.merge(
            history, how="left", left_on="id_es", right_on="problem_id"
        ).drop_duplicates("sentence_es")

        # count tokens sort
        joined["tokens"] = joined["sentence_es"].astype(str).str.split().apply(len)

        revision_order = ["last_n", "fail_count", "tokens"]
        revision_asc = [True, False, True]
        learning_order = ["tokens"]
        learning_asc = [True]

        order = revision_order if revision_mode else learning_order
        asc = revision_asc if revision_mode else learning_asc

        final = joined.sort_values(by=order, ascending=asc)

        return final

    def get_question(self) -> Generator[Question, Question, Question]:
        """Return a question from a given dataset."""

        revision = True if self.sorting_mode == STYPES.PRACTICE_MODE else False
        sorting = self.sorting(revision_mode=revision)

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

    questions = QuestionEngine(history=TrackingInterface(), game_mode="sentences")

    this_question = questions.get_question()

    a = next(this_question)
    b = next(this_question)
    c = next(this_question)
    d = next(this_question)

    breakpoint()
