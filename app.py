from csv import reader
import os
from random import choice

from flask import Flask, request, Response
import requests

app = Flask(__name__)
GROUPME = 'https://api.groupme.com/v3/bots/'
MAX_CHARS = 1000
PASTA_FILE = 'pastas.csv'


@app.route('/api/')
def hello_world():
    return 'Hello, World!'


@app.route('/api/keckbot/', methods=['POST'])
def keckbot(): 
    keckbot_id = "98a6e8591e0f1659353b463305"
    input_body = request.json
    possible_responses = ['on track', 'good', 'uncertain', 'chaotic', 'accelerating', 'not good', 'not on track', 'not accelerating', 'progressing', 'not progressing']
    
    message = f"progress is {choice(possible_responses)}."

    if '@keckbot' in input_body["text"]:
        body = {"bot_id": keckbot_id, "text": message}
        resp = requests.post(GROUPME + 'post', data=body)
        if not resp.ok:
            raise ValueError(resp)

    return Response(message)


def _get_message(input_body):
    text = input_body['text']
    name = input_body.get('name')
    
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


def break_string(string):
    return [string[i:i + MAX_CHARS] for i in range(0, len(string), MAX_CHARS)]


@app.route('/api/rybot/', methods=['POST'])
def rybot():
    rybot_id = '918ba2a82ce55dee51f94931f2'
    input_body = request.json
    message = _get_message(input_body)

    if '@RyBot' in input_body["text"]:
        body = {"bot_id": rybot_id, "text": message}
        resp = requests.post(GROUPME + 'post', data=body)
        if not resp.ok:
            raise ValueError(resp)

    return Response(message)


def _read_pastas():
    with open(PASTA_FILE, 'r', encoding='latin-1') as csv:
        content = reader(csv)
        pastas = {row[0]: row[1] for row in content}
    return pastas

@app.route('/api/pastabot/', methods=['POST'])
def pastabot():
    pastabot_id = 'c04d758189c5de3217830372ac'  # test
    # pastabot_id = '990d346038746d572fe9d6146b'
    pastas = _read_pastas()

    input_body = request.json
    message = ''
    text = input_body["text"]

    if '@pastabot' in text:
        for key in pastas.keys():
            if key in text:
                message = pastas[key]
                break
        if not message and 'random' in text:
            message = choice(list(pastas.values()))
        elif not message and 'keys' in text:
            message = ', '.join(list(pastas.keys()))

        broken_string = break_string(message)
        for string in broken_string:
            body = {"bot_id": pastabot_id, "text": string}
            resp = requests.post(GROUPME + 'post', data=body)
            if not resp.ok:
                raise ValueError(resp)

    return Response(message)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
