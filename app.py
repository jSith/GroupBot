import os
from random import choice

from flask import Flask, request, Response
import requests

app = Flask(__name__)
BOT_ID = 'b5d3d53337307f218d593c7b1b'
GROUPME = 'https://api.groupme.com/v3/bots/'

@app.route('/api/')
def hello_world():
    return 'Hello, World!'

def _get_message(inputBody): 
    text = inputBody['text']
    name = inputBody.get('name')
    
    response_messages = ['Yes', 'No', 'Maybe', 'Alright', 'A debilitating surgery would']
    neutral_messages = ['Okay', 'Thanks', 'Try it again']
    all_messages = response_messages + neutral_messages
    
    message_base = ''
    if 'what can you say?' in text:
        message_base = ', '.join(all_messages)
    elif '?' in text: 
        message_base = choice(response_messages)
    else: 
        message_base = choice(neutral_messages)
    message = f'Hi {name}, \n {message_base} \n - RyBot'
    return message

@app.route('/api/rybot/', methods=['POST'])
def bot(): 
    inputBody = request.json
    if '@RyBot' in inputBody['text']:
        message = _get_message(inputBody)
        body = {'bot_id': BOT_ID, 'text': message}
        requests.post(GROUPME + 'post', data=body)
    
if __name__ == "__main__": 
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
