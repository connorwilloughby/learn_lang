import re

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class Translator:
    """The core class which handles all interactions with translations and maps"""

    def __init__(self) -> None:
        self.model = SentenceTransformer("distiluse-base-multilingual-cased-v2")

    def translate(self, a: str, b: str, a_src: str):
        """Determine the quality of a translation

        :param a: str: Target translation
        :param b: str: User translation
        :rtype np.float64(): user score
        """
        a_clean = re.sub(r"[!\"#$%&'()*+,\-./:;<=>?@\[\\\]^_`{|}~]+", "", a).lower()
        b_clean = re.sub(r"[!\"#$%&'()*+,\-./:;<=>?@\[\\\]^_`{|}~]+", "", b).lower()
        a_src_clean = re.sub(r"[!\"#$%&'()*+,\-./:;<=>?@\[\\\]^_`{|}~]+", "", a_src).lower()

        # skip if no attempt
        if b == "" or a == "" or b is None or a is None:
            return np.float64(0.0)

        # HACK: because i cba to do lemas rn
        if a_clean == b_clean:
            return np.float64(1.0)

        v1 = self.model.encode(a_clean)
        v2 = self.model.encode(a_src_clean)

        score = cosine_similarity([v1], [v2])[0][0]

        return score


if __name__ == "__main__":
    t_engine = Translator()

    # FIX: conjugation dimensions are fucked and hard
    string_1 = t_engine.translate(a="Ríndanse", b="Give it up.")
    string_3 = t_engine.translate(a="Átame.", b="Tie me up.")
    string_3 = t_engine.translate(a="Pienso, luego existo", b="I think therefore i am")

    breakpoint()
