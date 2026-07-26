"""Holds grading models which determine the difficulty of held data with CEFR outputs."""


class GradingEngine:
    """Responsible for managing the grading of problems"""

    def __init__(
        self,
    ):
        pass

    def evaluate(self, sentence: str) -> int:
        """Determine the difficulty of given sentences.

        Args:
            sentence: str

        """
        return len(sentence.split(" "))


if __name__ == "__main__":
    grader = GradingEngine()

    easy = "Cats are dogs"
    med = "German shepherds are dogs"
    hard = "my phone is a computer "

    result_1 = grader.evaluate(easy)
    result_2 = grader.evaluate(med)
    result_3 = grader.evaluate(hard)

    breakpoint()
