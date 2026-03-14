from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class Translator:
    """The core class which handles all interactions with translations and maps"""

    def __init__(self) -> None:
        self.model = SentenceTransformer("distiluse-base-multilingual-cased-v2")

    def translate(self, a: str, b: str):
        """Taking the two paramaters and evaluating the strenght of the translation within it"""

        v1 = self.model.encode(a)
        v2 = self.model.encode(b)

        score = cosine_similarity([v1], [v2])[0][0]

        return score


if __name__ == "__main__":

    t_engine = Translator()

    string_1 = t_engine.translate("casa", "house")
    string_2 = t_engine.translate("casa", "home")
    string_3 = t_engine.translate("abajo", "below")
    string_4 = t_engine.translate("abajo", "under")
    string_5 = t_engine.translate("alguien", "something")

    breakpoint()
