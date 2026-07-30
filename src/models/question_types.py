from pydantic import BaseModel


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
    alternatives: list[str] = []


class QuestionStats(BaseModel):
    """User history statistics within a given problem!"""

    problem_id: int
    correct_count: int
    fail_count: int
    attempts: int
    pass_rate: float
