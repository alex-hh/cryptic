import argparse
import json
import os


def main(args):
    metrics, answers = evaluation.run(model)
    if args.output_dir is not None:
        output_dir = os.path.join(args.output_dir, f"{args.evaluation_name}/{args.model_name}")
        json.dump(metrics, os.path.join(output_dir, "metrics.json"))
        answers.to_csv(os.path.join(output_dir, "answers.csv"), index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("evaluation_name")
    parser.add_argument("model_name")
    parser.add_argument("--output_dir", default=None)
    args = parser.parse_args()
    main(args)
