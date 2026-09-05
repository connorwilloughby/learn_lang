import pandas as pd
from datasets import load_dataset

from config.config import ConfigWork

shared_config = ConfigWork


class HuggingFaceSource:
    """Returns a dataset from any given hugging face source"""

    def __init__(self, source_location: str, save_location: str):

        self.source_location = source_location
        self.save_location = f"./{save_location}"

    def download(self):
        """Return the file from HF and saves it to the disk"""
        raw = load_dataset(self.source_location)

        raw.save_to_disk(self.save_location)

    def load(self) -> pd.DataFrame:
        """Return the data set a `pd.DataFrame`"""
        return pd.read_parquet(self.save_location, engine="pyarrow")


class TargetWords(HuggingFaceSource):
    """Returns a dataset containing words."""

    def __init__(self):
        self.source_location = shared_config.SENTENCE_SOURCE
        self.save_location = shared_config.SENTENCE_WRITE_LOCATION

    def load(self) -> pd.DataFrame:
        """Load the local csv with many assumptions."""
        set = pd.read_csv(
            self.save_location,
            sep="\t",
            names=[
                "id_es",
                "sentence_es",
                "id_en",
                "sentence_en",
            ],
        )

        set["tokens"] = set["sentence_es"].astype(str).str.split().apply(len)
        set = set[set["tokens"] == 1]

        set.drop_duplicates(subset=["sentence_es"], keep="first")


class TargetSentencePartial(HuggingFaceSource):
    """Sentences in both languages with a missing word that as to be inserted!"""

    def __init__(self):
        self.source_location = shared_config.SENTENCE_SOURCE
        self.save_location = shared_config.SENTENCE_WRITE_LOCATION

    def load(self) -> pd.DataFrame:
        """Load the local csv with many assumptions."""
        set = pd.read_csv(
            self.save_location,
            sep="\t",
            names=[
                "id_es",
                "sentence_es",
                "id_en",
                "sentence_en",
            ],
        )

        set["tokens"] = set["sentence_es"].astype(str).str.split().apply(len)
        set = set[set["tokens"] >= 3]

        set.drop_duplicates(subset=["sentence_es"], keep="first")

        return set.sample(frac=1)


class TargetSentencesFull:
    """Returns a dataset containing sentences."""

    def __init__(self):
        self.source_location = shared_config.SENTENCE_SOURCE
        self.save_location = shared_config.SENTENCE_WRITE_LOCATION
        self.load()
        self.set = self.sentences_filter()

    def load(self) -> pd.DataFrame:
        """Load the local csv with many assumptions."""
        frame = pd.read_csv(
            self.save_location,
            sep="\t",
            names=[
                "id_es",
                "sentence_es",
                "id_en",
                "sentence_en",
            ],
        )

        # get sentence tokens
        frame["tokens"] = frame["sentence_es"].astype(str).str.split().apply(len)

        # HACK: this is likely going to cause issues later with alternative options
        # this is needed as the set has two paths that it can fall down
        frame.drop_duplicates(subset=["sentence_es"], keep="first")

        return frame

    def sentences_filter(self):
        """Filter out single token objects within `sentence_es`"""
        df = self.set
        return df[df["tokens"] >= 2]


class TargetMissingWord(TargetSentencesFull):
    """Returns a dataset containing sentences but with a missing word."""

    def __init__(self):

        _ = super().__init__

        self.set = self.missing_sen_filter()

    def missing_sen_filter(self) -> pd.DataFrame:
        """Create a set by removing desirable words"""
        _ = self.set

        return NotImplementedError


if __name__ == "__main__":
    s = TargetSentencesFull().load()
    # _ = TargetWords().download()
    # w = TargetWords().load()
    # _ = TargetSentences().download()

    breakpoint()
