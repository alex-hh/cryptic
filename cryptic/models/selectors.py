import pandas as pd


class BaseSelector:
    pass


class SelfConsistencySelector:

    def __init__(self, validator_names):
        self.validator_names = validator_names

    def select(self, answer_df):
        pred_cols = [
            "prediction",
            "predicted_definition",
            "wordplay"
        ] + self.validator_names + ["prediction_satisfies_constraints"]
        long_df = pd.wide_to_long(answer_df, pred_cols, i="rowid", j="index", sep="-")
        query = ' & '.join(self.validator_names + ["prediction_satisfies_constraints"])
        filtered_df = long_df.query(query).reset_index()
        selected_df = filtered_df.groupby("rowid").head(1)
        return selected_df
