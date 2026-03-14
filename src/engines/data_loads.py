import pandas as pd

from datasets import load_dataset


# fuck you https://huggingface.co/datasets/omar95/wikimedia_es_words_filtered_only_spanish_letters
# 'pd.read_parquet("hf://datasets/omar95/wikimedia_es_words_filtered_only_spanish_letters/data/train-00000-of-00001.parquet").to_parquet("data/fuck.parquet")


class TargetWords:

    def __init__(self) -> None:
        pass

    def download(self):

        raw = load_dataset(
            "omar95/wikimedia_es_words_filtered_only_spanish_letters/data/train-00000-of-00001.parquet"
        )

        raw.save_to_disk("data/source.arrow")

    def load(self):

        return pd.read_parquet("data/fuck.parquet", engine="pyarrow")


if __name__ == "__main__":

    a = TargetWords().load()

    breakpoint()
