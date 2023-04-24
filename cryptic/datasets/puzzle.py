import json
import re
import random
import numpy as np
import pandas as pd


def mask_word(word, rng=None):
    # q. how do masked words get tokenised
    L = len(word)
    num_mask = random.randint(L)
    if rng is None:
        rng = np.default_rng()
    mask_ids = rng.choice(L, num_mask, replace=False)
    masked_word = ""
    for i, char in enumerate(word):
        if i in mask_ids:
            masked_word += "_"
        else:
            masked_word += char
    return masked_word


def extract_num_letters(clue):
    """Assumes number of letters provided in brackets at end of clue.

    e.g. (8), (3,5) -- without spaces.

    Seems to conform with (at least some?) of George Ho's dataset
    """
    match = re.search("\([\d,]+\)$", clue)
    if match:
        num_letters = eval(match.group(0))
    else:
        num_letters = None
    return num_letters


class PuzzleFrame:

    """Wrapper for a dataframe containing a puzzle.

    Required Cols:
    clue, answer, num_letters, definition
    """

    def __init__(self, df):
        self.df = df


class QAFrame:

    """Wrapper for a dataframe containing question-answer pairs.

    Required Cols:
    question, answer, num_letters, definition
    """

    def __init__(self, df):
        self.df = df

    def mask_answers(self):
        df = self.df.copy()
        df["answer"] = df["answer"].apply(mask_word)
        return df

    @classmethod
    def from_gh_csv(cls, csv_filename):
        """Loads a dataframe from George Ho's website into standardized format."""
        df = pd.read_csv(csv_filename)
        df["num_letters"] = df["clue"].apply(extract_num_letters)
        df = df[~df["num_letters"].isnull()]
        return cls(df)

    @classmethod
    def from_interface_json(cls, json_filename):
        df = pd.read_json(json_filename)
        df["num_letters"] = df["num_letters"].apply(lambda x: tuple(x) if isinstance(x, list) else x)
        df["rowid"] = np.arange(len(df))
        return cls(df)

    @classmethod
    def from_quiptic_json(cls, json_filename):
        with open(json_filename, "r") as f:
            d = json.load(f)
        df = pd.DataFrame.from_records(d["clues"])
        df["num_letters"] = df["num_letters"].apply(lambda x: x[0] if len(x)==1 else tuple(x))  # todo standardise this
        df["rowid"] = np.arange(len(df))
        return cls(df)

    def sample(self, num_clues):
        df = self.df.sample(num_clues)
        return QAFrame(df)
