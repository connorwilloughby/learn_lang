from typing import Any, Optional

from pydantic import BaseModel


class TranslationInput(BaseModel):
    """The required parameters for the `TranslationEngine`"""

    target_word: str
    user_solution: str


class TranslationResponse(BaseModel):
    """Response type from `TranslationEngine().translate(a, b)`"""

    accuracy: Any
    user_solution: str
    solution: str
    alternatives: Optional[list[str]] = [""]
