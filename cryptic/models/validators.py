class BaseValidator:

    """A validator takes as input a prediction and an explanation.
    
    This is currently different from explicit constraint checks.
    """

    def validate(self, prediction, explanation):
        raise NotImplementedError()


class SubWordConsistencyValidator:

    """Check that subwords actually add up to answer.

    We ignore order by default.
    """

    def __init__(self, prompt_interface, fix_order=False):
        self.prompt_interface = prompt_interface
        self.fix_order = fix_order

    def validate(self, prediction, definition, wordplay):
        units = self.prompt_interface.decompose(wordplay)
        subwords = [unit["answer"] if unit is not None else "" for unit in units]
        concat = "".join(subwords)
        if self.fix_order:
            return concat == prediction
        else:
            return sorted(list(concat)) == sorted(list(prediction))
