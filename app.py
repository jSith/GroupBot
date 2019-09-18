import os
from random import choice

from flask import Flask, request, Response
import requests

app = Flask(__name__)
BOT_ID = '7af5564a9760b445535c79bc3a'
GROUPME = 'https://api.groupme.com/v3/bots/'

@app.route('/api/')
def hello_world():
    return 'Hello, World!'

def _get_message(text): 
    response_messages = ['Yes', 'No', 'Maybe', 'A debilitating surgery would']
    neutral_messages = ['Okay', 'Thanks']
    message_base = ''
    if '?' in text: 
        message_base = choice(response_messages)
    else: 
        message_base = choice(neutral_messages)
    message = message_base + ' - RyBot'
    return message

@app.route('/api/rybot/', methods=['POST'])
def bot(): 
    input = request.json
    if '@RyBot' in input['text']: 
        message = _get_message(input['text'])
        body = {'bot_id': BOT_ID, 'text': message}
        requests.post(GROUPME + 'post', data=body)
    
if __name__ == "__main__": 
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
