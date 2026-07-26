import pandas as pd
from datasets import load_dataset

from src.config.config import ConfigWork

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
        super().__init__(
            source_location=shared_config.WORD_SOURCE,
            save_location=shared_config.WORD_WRITE_LOCATION,
        )


class TargetSentences:
    """Returns a dataset containing sentences."""

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
        
        # HACK: this is likely going to cause issues later with alternative options
        # this is needed as the set has two paths that it can fall down
        set.drop_duplicates(subset=["sentence_es"], keep="first")

        return set.sample(frac=1)


if __name__ == "__main__":
    s = TargetSentences().load()
    # _ = TargetWords().download()
    # w = TargetWords().load()
    # _ = TargetSentences().download()

    breakpoint()
