import re

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class Translator:
    """The core class which handles all interactions with translations and maps"""

    def __init__(self) -> None:
        self.model = SentenceTransformer("distiluse-base-multilingual-cased-v2")

    def translate(self, a: str, b: str):
        """Determine the quality of a translation

        :param a: str: Target translation
        :param b: str: User translation
        :rtype np.float32(): user score
        """
        a_clean = re.sub(r"[^\w\s]", "", a).lower()
        b_clean = re.sub(r"[^\w\s]", "", b).lower()

        if a_clean == b_clean:
            return 1.0

        v1 = self.model.encode(a_clean)
        v2 = self.model.encode(b_clean)

        score = cosine_similarity([v1], [v2])[0][0]

        return score


if __name__ == "__main__":
    t_engine = Translator()

    string_1 = t_engine.translate("casa", "house")
    string_2 = t_engine.translate("casa", "home")
    string_3 = t_engine.translate("abajo", "below")
    string_3 = t_engine.translate("Beberlo.", "drink it")
    string_4 = t_engine.translate("abajo", "under")
    string_5 = t_engine.translate("alguien", "something")
    breakpoint()
