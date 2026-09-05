"""A store for the various information we have on game types"""


class GameTypes:
    """Holds various options for game types"""

    def __init__(self):

        self.SENTENCE_MODE: int = 1
        """"""
        self.WORD_MODE: int = 2
        """"""


class SortingTypes:
    """Hold various options for sorting types"""

    def __init__(self):
        self.LEARNING_MODE: int = 1
        """"""
        self.PRACTICE_MODE: int = 2
        """"""
