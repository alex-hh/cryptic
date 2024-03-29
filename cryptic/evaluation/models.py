from functools import partial
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


def constraint_check(prediction, num_letters, partial_clue=None):
    letter_counts = tuple([len(w) for w in prediction.split(" ")])
    if partial_clue is not None:
        raise NotImplementedError()

    if len(letter_counts) == 1:
        return letter_counts[0] == num_letters
    else:
        return letter_counts == num_letters


def reconstruct_from_decomposition(row, i):
    pred = row[f"prediction-{i}"]
    definition = row[f"predicted_definition-{i}"]
    wordplay = row[f"wordplay-{i}"]
    return f"{pred} ({definition}) - {wordplay}"


class QAModel:

    def predict(self, df, num_answers=1):
        df = df.copy()
        all_outputs = self.predict_n(df, num_answers)

        prediction_cols = [f"prediction-{i}" for i in range(num_answers)]
        if isinstance(all_outputs[0][0], str):
            answers_df = pd.DataFrame(all_outputs, columns=prediction_cols)
            df[prediction_cols] = answers_df[prediction_cols].values

        elif isinstance(all_outputs[0][0], dict):

            for k in all_outputs[0][0].keys():
                if k == "answer":
                    col_name = "prediction"
                else:
                    col_name = k
                values = [[d[k] for d in answer_list] for answer_list in all_outputs]
                cols = [f"{col_name}-{i}" for i in range(num_answers)]
                vals_df = pd.DataFrame(values, columns=cols)
                df[cols] = vals_df[cols].values

        else:
            raise ValueError()

        # TODO somehow handle letter constraints in qaframe
        for i, pred_col in enumerate(prediction_cols):
            df[f"prediction_satisfies_constraints-{i}"] = df.apply(
                lambda row: constraint_check(row[pred_col], row["num_letters"]),
                axis=1
            )

            reconstructor = partial(reconstruct_from_decomposition, i=i)
            df[f"reconstruction-{i}"] = df.apply(reconstructor, axis=1)

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
