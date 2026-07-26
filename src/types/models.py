from typing import Any, Optional

from pydantic import BaseModel


class PlayerStatistics(BaseModel):
    """Tracks information about the player stats"""

    streak: int


class QuestionHistory(BaseModel):
    """Recent performance on certain words and their answers"""

    problem_id: int
    correct_count: int
    fail_count: int


class Question(BaseModel):
    """Used to store problems and solutions"""

    _table_name: str = "question_history"

    problem_id: int
    problem: str
    solution: str



class QuestionStats(BaseModel):
    """User history statistics within a given probelem!"""

    problem_id: int
    correct_count: int
    fail_count: int
    attempts: int
    pass_rate: float



class TranslationInput(BaseModel):
    """The required parameters for the `TranslationEngine`"""

    target_word: str
    user_solution: str


class TranslationResponse(BaseModel):
    """Response type from `TranslationEngine().translate(a, b)`"""

    accuracy: Any
    user_solution: str
    solution: str
    synonyms: Optional[list[str]] = [""]

