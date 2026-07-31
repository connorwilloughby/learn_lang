"""Stores unittest relating to the translator class"""

import unittest
from unittest.mock import MagicMock, patch

from engines.translator import Translator


class TestTranslator(unittest.TestCase):
    """Holds unit tests for the translation method on Translator"""

    def test_ident_override(self):
        """Assert that when receiving a perfect translation we skip to return 1.0"""
        # arrange
        encode_mocks = [
            [
                [0.9, 0.9],
            ],
        ]

        mock_transformer = MagicMock(return_value=MagicMock)
        with patch("engines.translator.SentenceTransformer", return_values=mock_transformer) as _:
            translator = Translator()
        translator.model = mock_transformer
        translator.model.encode = MagicMock(side_effect=encode_mocks)

        # act
        score = translator.translate(a="hey", a_src="Hey", b="Hola")

        # assert
        assert score == 1.0

    def test_basic_translate(self):
        """Assert that when receiving a very close match we return a float for this."""
        # arrange
        encode_mocks = [
            [0.9, 0.9],
            [0.9, 0.8],
        ]

        mock_transformer = MagicMock(return_value=MagicMock)
        with patch("engines.translator.SentenceTransformer", return_values=mock_transformer) as _:
            translator = Translator()
        mock_transformer = MagicMock(return_value=MagicMock)
        translator.model = mock_transformer
        translator.model.encode = MagicMock(side_effect=encode_mocks)

        # act
        score = translator.translate(a="Good morning", a_src="Morning", b="Buenas días.")

        # assert

        assert score == 0.9982743731749959


if __name__ == "__main__":
    unittest.main()
