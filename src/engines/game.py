import numpy as np

from config.config import ConfigWork
from engines.question import QuestionEngine
from engines.translator import Translator
from interfaces.console import ConsoleInterface
from interfaces.tracking import TrackingInterface
from models.exception_types import GameMenuChange
from models.game_types import GameTypes, SortingTypes
from models.translation_types import TranslationResponse
from utilities.text_utils import color_wrap

CONFIG = ConfigWork()
STYPES = SortingTypes()
GTYPES = GameTypes()


class GameEngine:
    """Instructs all child classes and orchestrates the game"""

    def __init__(self) -> None:

        self.statistics = TrackingInterface()
        self.question_engine = QuestionEngine(history=self.statistics)
        self.translation_engine = Translator()
        self.interface = ConsoleInterface()

    @staticmethod
    def _translation_grade(score: np.float32) -> bool:
        """Evaluate if a given score should be considered as a pass

        Params:
            score (np.float32)
        """
        return bool(score >= CONFIG.TRANSLATION_PASSING_GRADE)

    def handle_menu(self):
        """Enable the user to interface with game modes and handle changes between them"""
        try:
            # offer user the game
            game_mode = int(ConsoleInterface().menu_mode())
            sort_mode = int(ConsoleInterface().menu_sort())

            # sentence mode
            if game_mode == GTYPES.SENTENCE_MODE:
                # HACK make this an enum not string on target
                self.question_engine = QuestionEngine(
                    sorting=sort_mode, history=self.statistics, game_mode="sentences"
                )
                self.handle_game()
            # word mode
            if game_mode == GTYPES.WORD_MODE:
                self.question_engine = QuestionEngine(
                    sorting=sort_mode, history=self.statistics, game_mode="words"
                )
                self.handle_game()
        except GameMenuChange:
            self.handle_menu()

    def handle_game(self, mode: int = 0):
        """Manage the main gameplay loop"""
        # allow the iterator to persist across questions
        question_state = self.question_engine.get_question()

        while True:
            # prepare a question
            question = next(question_state)
            stats = self.statistics.get_problem_stats(problem_id=question.problem_id)

            # ask a question
            user_response = self.interface.question(question=question, stats=stats)

            # score the translation
            score = self.translation_engine.translate(
                a=user_response, a_src=question.solution, b=question.problem
            )

            # TODO: tell the user if it was right...
            # convert the score to bool
            accurate_translation = self._translation_grade(score)

            # record this result
            self.statistics.upsert_problem_stats(
                problem_id=question.problem_id, correct=accurate_translation
            )

            #  review the attempt
            self.interface.review(
                TranslationResponse(
                    accuracy=accurate_translation,
                    user_solution=user_response,
                    solution=question.solution,
                    problem=question.problem,
                    alternatives=question.alternatives,
                )
            )
