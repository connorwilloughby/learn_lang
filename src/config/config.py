class ConfigWork:
    """Stores all shared variables which are expected to be referenced in multiple locations."""

    TRANSLATION_PASSING_GRADE: float = 0.86

    # used to configure the setup of the sentence data
    SENTENCE_SOURCE: str = "tatoeba.org/en/downloads"
    SENTENCE_WRITE_LOCATION: str = "data/sentences/spanish_english.tsv"

    # used to configure the location of the word data
    WORD_SOURCE: str = "omar95/wikimedia_es_words_filtered_only_spanish_letters/data/train-00000-of-00001.parquet"
    WORD_WRITE_LOCATION: str = "data/words/word_sources.arrow"

    def log(self):

        string = f"""All config: 

SENTENCE_SOURCE {self.SENTENCE_SOURCE}
SENTENCE_WRITE_LOCATION {self.SENTENCE_WRITE_LOCATION}
WORD_SOURCE {self.WORD_SOURCE}
WORD_WRITE_LOCATION {self.WORD_WRITE_LOCATION}
"""

        print(string)


if __name__ == "__main__":
    ConfigWork()
