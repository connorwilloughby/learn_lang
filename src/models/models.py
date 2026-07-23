from typing import Any, Optional

import numpy as np
from pydantic import BaseModel


class PlayerStatistics(BaseModel):
    """Tracks information about the player stats"""

    streak: int


class QuestionHistory(BaseModel):
    """Recent performance on certain words and their answers"""

    word: str
    answer: str
    state: str


class Question(BaseModel):
    """Used to store problems and solutions"""

    problem: str
    solution: str
    # alternatives: Optional[str]


class TranslationInput(BaseModel):
    """The required parameters for the `TranslationEngine`"""

    target_word: str
    user_solution: str


class TranslationResponse(BaseModel):
    """Response type from `TranslationEngine().translate(a, b)`"""

    accuracy: Any
    user_solution: str
    solution: str
    synonyms: Optional[list[str]] = ''
