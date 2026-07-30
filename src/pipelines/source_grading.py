from engines.grader import GradingEngine
from sources.sources import TargetSentences


def grade_sp_en_sentences():
    """Import the sentence data and add a grading to it"""
    sentences_df = TargetSentences().load()
    grader = GradingEngine()

    for row in sentences_df.iterrows():
        # HACK: why does this slice?
        _ = grader.evaluate(row[1].sentence_es)

        pass


if __name__ == "__main__":
    grade_sp_en_sentences()

    breakpoint()
