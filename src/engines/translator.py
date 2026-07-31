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
        a_src_clean = re.sub(r"[!\"#$%&'()*+,\-./:;<=>?@\[\\\]^_`{|}~]+", "", a_src).lower()

        # HACK: because i cba to do lemas rn
        if a_clean == a_src_clean:
            return np.float64(1.0)

        v1 = self.model.encode(a_clean)
        v2 = self.model.encode(a_src_clean)

        score = cosine_similarity([v1], [v2])[0][0]

        return score


if __name__ == "__main__":
    t_engine = Translator()

    string_3 = t_engine.translate(
        "why are you reading this? you stalking me bro? offer me a job i could do with it.\
              FIND ME ON LINKED IN! PLEASE!",
        "¿Por qué estás leyendo esto? ¿Me estás acosando, tío? Ofréceme un trabajo, me \
            vendría bien. ¡BÚSCAME EN LINKEDIN! ¡POR FAVOR!",
        "¿Por qué estás leyendo esto? ¿Me estás acosando, tío? Ofréceme un trabajo, me \
            vendría bien. ¡BÚSCAME EN LINKEDIN! ¡POR FAVOR!",
    )
    # FIX: conjugation dimensions are fucked and hard
    string_1 = t_engine.translate("Ríndanse", "Give it up.")
    string_3 = t_engine.translate("Átame.", "Tie me up.")
    string_3 = t_engine.translate("Pienso, luego existo", "I think therefore i am")

    breakpoint()
