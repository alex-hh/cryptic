import os
import openai


openai.api_key = os.getenv("OPENAI_API_KEY")
BASEDIR = os.path.dirname(os.path.dirname(__file__))