"""A store for the various information we have on game types"""


class GameTypes:
    """Defines the various gametypes as an enum"""

    def __init__(self):

        self.SENTENCE_MODE: int = 1
        """The game mode for translating sentences"""
        self.WORD_MODE: int = 2
        """The game mode for translating words"""


class SortingTypes:
    """Defines the sorting types and their values"""

    def __init__(self):
        self.LEARNING_MODE: int = 1
        """The game mode for expanding problems"""
        self.PRACTICE_MODE: int = 2
        """The game mode for revising historically difficult words"""
