import os
import openai
from dotenv import load_dotenv

load_dotenv() # load environment variables from .env file
openai.api_key = os.getenv("OPENAI_API_KEY") # set OpenAI API key
model = os.getenv("GPT_MODEL") # get GPT model from environment variables

def get_completion_from_messages(messages, model=model, temperature=0):
    # Call the OpenAI API to generate a completion based on the provided messages
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    # Extract the generated completion from the API response
    return response.choices[0].message["content"]
