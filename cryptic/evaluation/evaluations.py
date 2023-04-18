from cryptic.datasets.puzzle import QAFrame


evaluations = {}


class EvaluationSpec:

    def __init__(self, entrypoint, kwargs):
        self.entrypoint = entrypoint
        self.kwargs = kwargs

    def make(self):
        return self.entrypoint(**self.kwargs)


class QAEvaluation:

    def __init__(self, qa_frame, num_answers=1):
        self.qa_frame = qa_frame
        self.num_answers = num_answers

    def run(self, qa_model):
        answer_frame = qa_model.predict(self.qa_frame.df, num_answers=self.num_answers)
        prediction_cols = [f"prediction-{i}" for i in range(self.num_answers)]
        correct_answers = answer_frame[prediction_cols].values == answer_frame["answer"].values[:, None]
        any_correct = correct_answers.any(-1)
        num_correct = correct_answers.sum(-1)
        answer_frame["correct"] = any_correct
        answer_frame["num_correct"] = num_correct
        return {"accuracy": answer_frame["correct"].sum() / len(answer_frame)}, answer_frame


class GeorgeHoQA(QAEvaluation):

    def __init__(self, csv_filename, num_answers=1, num_clues=None, puzzle_name=None):
        qa_frame = QAFrame.from_gh_csv(csv_filename)
        if puzzle_name is not None:
            qa_frame = QAFrame(qa_frame.df[qa_frame.df["puzzle_name"]==puzzle_name])
        if num_clues is not None:
            qa_frame = qa_frame.sample(num_clues)
        super().__init__(qa_frame, num_answers=num_answers)


class MetroQA(QAEvaluation):

    def __init__(self, json_filename, num_answers=1, num_clues=None):
        qa_frame = QAFrame.from_json(json_filename)
        if num_clues is not None:
            qa_frame = qa_frame.sample(num_clues)
        super().__init__(qa_frame, num_answers=num_answers)


evaluations["Page1Example-n1"] = EvaluationSpec(
    GeorgeHoQA, dict(csv_filename="data/examples/gh_page1.csv")
)
evaluations["Page1Example-n10"] = EvaluationSpec(
    GeorgeHoQA, dict(csv_filename="data/examples/gh_page1.csv", num_answers=10)
)
evaluations["QC-1711"] = EvaluationSpec(
    GeorgeHoQA, dict(csv_filename="data/examples/qc_1711.csv", num_answers=5)
)


def get(name):
    return evaluations[name].make()
