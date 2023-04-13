import tqdm
import openai
from cryptic.evaluation.models import QAModel


class OpenAIQA(QAModel):

    def __init__(self, prompt_interface, model_name, temperature=0.6, max_tokens=16):
        self.prompt_interface = prompt_interface
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens

    def get_response(self, clue, num_letters, num_answers=1):
        prompt = self.prompt_interface.inject_prompt(clue, num_letters)
        response = openai.Completion.create(
            model=self.model_name,
            prompt=prompt,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            n=num_answers,
            # logprobs=5,  might be interesting to use -- gives some kind of per token probs (with alternatives)
        )
        return response

    def answers_from_response(self, response):
        return [self.prompt_interface.extract_answer(choice["text"]) for choice in response["choices"]]
        # return [choice["text"].replace("\n", "").upper() for choice in response["choices"]]

    def predict_n(self, df, num_answers=1):
        all_answers = []
        for clue, num_letters in tqdm.tqdm(zip(df["clue"].values, df["num_letters"].values)):
            response = self.get_response(clue, num_letters, num_answers=num_answers)
            answers = self.answers_from_response(response)
            all_answers.append(answers)
        return all_answers
