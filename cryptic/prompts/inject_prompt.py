import importlib


def format_num_letters(num_letters):
    if isinstance(num_letters, int):
        return f"({num_letters})"
    elif isinstance(num_letters, tuple):
        return str(num_letters)


def inject_prompt(prompt_name, clue, num_letters):
    module, obj = prompt_name.rsplit('.', 1)
    module = importlib.import_module(module)
    prompt = getattr(module, obj)

    return prompt.format(clue=clue, num_letters=format_num_letters(num_letters))
