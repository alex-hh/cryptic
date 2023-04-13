import importlib
import re


def format_num_letters(num_letters):
    if isinstance(num_letters, int):
        return f"({num_letters})"
    elif isinstance(num_letters, tuple):
        return str(num_letters)


def get_prompt_templates(prompt_name):
    module, obj = prompt_name.rsplit('.', 1)
    module = importlib.import_module(module)
    prompt = getattr(module, obj)
    return prompt


class PromptInterface:

    def __init__(self, prompt_name):
        self.prompt_templates = get_prompt_templates(prompt_name)

    def inject_prompt(self, clue, num_letters):
        prompt_template = self.prompt_templates["prompt"]
        return prompt_template.format(clue=clue, num_letters=format_num_letters(num_letters))

    def extract_answer(self, output):
        match = re.search(self.prompt_templates["answer_pattern"], output)
        output = {}
        if match:
            output["answer"] = match.group("answer")
            output["predicted_definition"] = match.group("definition")
            output["wordplay"] = match.group("wordplay")
        else:
            output["answer"] = ""
            output["predicted_definition"] = ""
            output["wordplay"] = ""
        return output

    def decompose(self, wordplay):
        decomposition = []
        for unit in wordplay.split(self.prompt_templates["subclue_separator"]):
            m = re.search(self.prompt_templates["sub_answer_pattern"], unit)
            if m:
                decomposition.append({"answer": m.group("answer"), "definition": m.group("definition")})
            else:
                decomposition.append(None)

        return decomposition
