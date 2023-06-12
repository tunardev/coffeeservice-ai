import json
from fastapi import FastAPI
from .models import Message
from .openai import get_completion_from_messages

app = FastAPI()

with open("app/context.json", "r") as file:
    json_data = file.read()

context = json.loads(json_data) # load the context from the JSON file
messages = context.copy() # initialize the messages list with the context

@app.get("/")
def all_messages():
    # Endpoint to retrieve all messages
    return messages[1:]

@app.post("/chat")
def chat(message: Message):
    # Endpoint to handle user chat messages
    messages.append({'role': 'user', 'content': message.content}) # add the user message to the messages list
    response = get_completion_from_messages(messages) # get the response from OpenAI
    messages.append({
        'role': 'assistant',
        'content': response
    })
    return {'answer': response, 'messages': messages[1:]}

@app.post("/buy")
def buy_coffee():
    # Endpoint to handle buying coffee
    messages.append({
        'role': 'system',
        'content': 'Create a JSON summary of the previous coffee order. Itemize the price for each item. '
                   'The fields should be 1) coffee, specify the drink type and size. '
                   '2) extras, list any additional extras or modifications for each drink. '
                   '3) snacks, specify the snack items and their quantities. '
                   '4) total price.'
    })
    response = get_completion_from_messages(messages) # get the response from OpenAI

    start_i = response.find('{')
    end_i = response.rfind('}')
    response = response[start_i:end_i+1]
    return {'result': json.loads(response)}

@app.post("/reset")
def reset():
    # Endpoint to reset the messages to the initial context
    messages = context
    return {'reset': 'success'}
