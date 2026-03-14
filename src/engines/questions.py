import pandas as pd

from src.engines.data_loads import TargetWords
from src.models.models import Question


class QuestionEngine:

    def __init__(self) -> None:

        self.questions: pd.DataFrame = TargetWords().load()

    def get_question(self):

        for question in self.questions.iterrows():

            yield Question(target_word=question[1].word, answer="BREAK")

if __name__ == "__main__":

    questions = QuestionEngine()

    this_quetion = questions.get_question()

    a = next(this_quetion)
    b = next(this_quetion)

    breakpoint()
