import pandas as pd
import numpy as np
import string


class ModelSpec:

    def __init__(self, entrypoint, kwargs):
        self.entrypoint = entrypoint
        self.kwargs = kwargs

    def make(self):
        return self.entrypoint(**self.kwargs)


models = {}


def randstring(n, to_upper=False):
    if isinstance(n, int):
        letters = np.random.choice(list(string.ascii_lowercase), n, replace=True)
        s = "".join(list(letters))
    elif isinstance(n, tuple):
        s = " ".join([randstring(_n) for _n in n])
    else:
        s = None
    if s is not None and to_upper:
        return s.upper()


class QAModel:

    def predict(self, df, num_answers=1):
        df = df.copy()
        answers = self.predict_n(df, num_answers)
        prediction_cols = [f"prediction_{i}" for i in range(num_answers)]
        answers_df = pd.DataFrame(answers, columns=prediction_cols)
        df[prediction_cols] = answers_df[prediction_cols].values
        return df

    def predict_n(self, df, num_answers):
        """Returns a list of lists of answers."""
        raise NotImplementedError()


class RandomStringModel(QAModel):

    def predict_n(self, df, num_answers):
        return list(df["num_letters"].apply(
            lambda x: [randstring(x, to_upper=True) for i in range(num_answers)]
        ).values)


class CheatingModel(QAModel):

    def predict_n(self, df, num_answers):
        return list(df["answer"].apply(lambda x: [x for i in range(num_answers)]).values)


models["RandomString"] = ModelSpec(RandomStringModel, dict())
models["Cheater"] = ModelSpec(CheatingModel, dict())


def get(name):
    return models[name].make()
