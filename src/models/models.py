from pydantic import BaseModel


class PlayerStatistics(BaseModel):
    """Tracks information about the player stats"""

    streak: int


class Question(BaseModel):
    target_word: str
    answer: str


class TranslationInput(BaseModel):
    target_word: str
    user_solution: str


class TranslationResponse(BaseModel):
    accuracy: bool
    user_solution: str
    synonyms: list[str]


class QuestionHistory(BaseModel):
    """Recent performance on certain words and their answers"""

    word: str
    answer: str
    state: str
