import pandas as pd


class BaseSelector:

    def make_long_df(self, answer_df):
        pred_cols = [
            "prediction",
            "predicted_definition",
            "wordplay",
            "response",
        ] + self.validator_names + ["prediction_satisfies_constraints"]
        long_df = pd.wide_to_long(answer_df, pred_cols, i="rowid", j="index", sep="-")
        return long_df


class SelfConsistencySelector(BaseSelector):

    """Apply constraints from letters (prediction satisfies constraints),
    and optionally from a list of boolean validators (e.g. a wordplay)
    consistency validator.
    """

    def __init__(self, validator_names):
        self.validator_names = validator_names

    def select(self, answer_df):
        long_df = self.make_long_df(answer_df)
        query = ' & '.join(self.validator_names + ["prediction_satisfies_constraints"])
        filtered_df = long_df.query(query).reset_index()
        selected_df = filtered_df.groupby("rowid").head(1)
        return selected_df


class RandomSelector:

    def select(self, answer_df):
        long_df = self.make_long_df(answer_df)
        selected_df = filtered_df.groupby("rowid").sample(1)
        return selected_df
