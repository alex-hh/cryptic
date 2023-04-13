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


class QAModel:

    def predict(self, df, num_answers=1):
        df = df.copy()
        all_outputs = self.predict_n(df, num_answers)
        if isinstance(all_outputs[0][0], str):
            print("string")
            prediction_cols = [f"prediction_{i}" for i in range(num_answers)]
            answers_df = pd.DataFrame(all_outputs, columns=prediction_cols)
        elif isinstance(all_outputs[0][0], dict):
            answers = [[d["answer"] for d in answer_list] for answer_list in all_outputs]
            prediction_cols = [f"prediction_{i}" for i in range(num_answers)]
            answers_df = pd.DataFrame(answers, columns=prediction_cols)

            if "explanation" in all_outputs[0][0]:
                explanations = [[d["explanation"] for d in answer_list] for answer_list in all_outputs]
                explanation_cols = [f"explanation_{i}" for i in range(num_answers)]
                exp_df = pd.DataFrame(explanations, columns=explanation_cols)
            else:
                print(answers[0][0], "no explanation")
        else:
            raise ValueError()

        df[prediction_cols] = answers_df[prediction_cols].values
        df[explanation_cols] = exp_df[explanation_cols].values
        # TODO somehow handle letter constraints in qaframe
        for pred_col in prediction_cols:
            df["satisfies_constraints"] = df.apply(lambda row: constraint_check(row[pred_col], row["num_letters"]), axis=1)
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
