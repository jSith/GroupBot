import os
from random import choice

from flask import Flask, request
import requests

app = Flask(__name__)
BOT_ID = '7af5564a9760b445535c79bc3a'
GROUPME = 'https://api.groupme.com/v3/bots/'

@app.route('/api/')
def hello_world():
    return 'Hello, World!'

def _get_message(): 
    possible_messages = ['Okay', 'No', 'Yes', 'A debilitating surgery would', 'Thanks']
    message_base = choice(possible_messages)
    message = message_base + ' - RyBot'
    return message

@app.route('/api/rybot/', methods=['POST'])
def bot(): 
    input = request.json
    message = _get_message()
    body = {'bot_id': BOT_ID, 'text': message}
    print(input)
    return input
    # requests.post(GROUPME + 'post', data=body)
    
if __name__ == "__main__": 
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
