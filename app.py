from base64 import b64encode
from csv import reader, writer
from difflib import get_close_matches
import os
from random import choice
import re

from flask import Flask, request, Response
import requests

GROUPME = 'https://api.groupme.com/v3'
GITHUB = 'https://api.github.com/repos/jSith/GroupBot'
MAX_CHARS = 1000
MEGACHAT_ID = 51117502
# MEGACHAT_ID = 53735323  # test
GIT_TOKEN = os.environ.get('GIT_TOKEN')
GROUPME_TOKEN = os.environ.get('GROUPME_TOKEN')
PASTABOT = os.environ.get('PASTABOT')
RYBOT = os.environ.get('RYBOT')
KECKBOT = os.environ.get('KECKBOT')
PASTA_FILE = 'pastas.csv'

app = Flask(__name__)


@app.route('/api/')
def hello_world():
    return 'Hello, World!'


@app.route('/api/immortalbot/')
def immortalbot():
    input_body = request.json
    raise NotImplementedError(input_body)


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


@app.route('/api/keckbot/', methods=['POST'])
def keckbot(): 
    input_body = request.json
    possible_responses = ['on track', 'good', 'uncertain', 'chaotic', 'accelerating', 'not good', 'not on track', 'not accelerating', 'progressing', 'not progressing']
    
    message = f"progress is {choice(possible_responses)}."

    if '@keckbot' in input_body["text"]:
        body = {"bot_id": KECKBOT, "text": message}
        resp = requests.post(f'{GROUPME}/bots/post', data=body)
        if not resp.ok:
            raise ValueError(resp)

    return Response(message)


def break_string(string):
    return [string[i:i + MAX_CHARS] for i in range(0, len(string), MAX_CHARS)]


@app.route('/api/rybot/', methods=['POST'])
def rybot():
    input_body = request.json
    message = _get_message(input_body)

    if '@RyBot' in input_body["text"]:
        body = {"bot_id": RYBOT, "text": message}
        resp = requests.post(f'{GROUPME}/bots/post', data=body)
        if not resp.ok:
            raise ValueError(resp)

    return Response(message)


def _read_pastas():
    with open(PASTA_FILE, 'r', encoding='utf-8') as csv:
        content = reader(csv)
        pastas = {row[0]: row[1].replace("\\n", "\n") for row in content}
    return pastas


def _update_git_file(new_key, new_value):
    file = requests.get(f'{GITHUB}/contents/{PASTA_FILE}',
                        headers={'Authorization': f'Bearer {GIT_TOKEN}'}).json()

    sha = file['sha']

    with open(PASTA_FILE, 'a', encoding='utf-8') as csv:
        csvwriter = writer(csv)
        csvwriter.writerow([new_key, new_value])

    with open(PASTA_FILE, 'r', encoding='utf-8') as csv:
        new_content = re.sub('\n', '\\n', csv.read())

    encoded_content = re.sub('^b\'|\'$', '', str(b64encode(new_content.encode('utf-8'))))
    msg = f"Add new pasta with key {new_key}"
    body = {"message": msg, "content": encoded_content, "sha": sha}

    resp = requests.put(f'{GITHUB}/contents/{PASTA_FILE}',
                        headers={'Authorization': f'Bearer {GIT_TOKEN}'},
                        json=body)

    return resp


def _add_new_pasta(text, uid, keys):
    key = re.search('key=(.*) value=', text).group(1)
    value = re.search('value=(.*)', text).group(1)

    if key in keys:
        message = f'Could not add this pasta because there is already a pasta with the key {key}.'
        return message
    elif 'keys' in key or 'random' in key or '@' in key:
        message = f'Could not add this pasta because the key {key} is a reserved word.'
        return message

    if 'lastlikedmessage' in value:
        last_messages = requests.get(f'{GROUPME}/groups/{MEGACHAT_ID}/messages?limit=100',
                                     headers={'X-Access-Token': GROUPME_TOKEN})
        if not last_messages.ok:
            message = f'Could not add a pasta because I could not find your last liked message. ' \
                f'I got this error: {last_messages.content}'
            return message

        last_liked_messages = list(filter(lambda msg: uid in msg['favorited_by'],
                                          last_messages.json()['response']['messages']))
        if not last_liked_messages:
            message = f'Could not add a pasta because I could not find your last liked message.'
            return message
        else:
            msg = last_liked_messages.pop(0)
            if msg['sender_type'] == 'bot':
                message = f'Could not add pasta because the sender of the last liked message was a bot'
                return message
            else:
                value = msg['text']

    if '@' in value:
        message = 'Could not add pasta because you cannot be trusted with the @ character'
        return message

    resp = _update_git_file(key, value)
    if not resp.ok:
        message = f'Could not add a pasta because there was an error with the Github API: {resp.content}'
    else:
        message = f'Successfully added pasta with key {key} and value {value}'

    return message


@app.route('/api/pastabot/', methods=['POST'])
def pastabot():
    input_body = request.json
    message = ''
    text = input_body["text"]
    uid = input_body["sender_id"]
    sender_type = input_body["sender_type"]

    if sender_type == "bot":
        return

    pattern = re.search('^@pastabot (.*)$', text)

    if pattern:
        pastas = _read_pastas()
        keys = list(pastas.keys())
        command = pattern.group(1)

        if re.search('^addpasta', command):
            if not re.search('^addpasta key=(.*) value=(.*)$', command):
                message = 'Could not add pasta because the addpasta command was incorrectly formatted.'
            else:
                try:
                    message = _add_new_pasta(text, uid, keys)
                except (KeyError, AttributeError) as e:
                    message = f'Could not add pasta because of error {e}'
        elif command == 'keys':
            message = ', '.join(keys)
        elif command == 'random':
            message = choice(list(pastas.values()))
        else:
            for key in keys:
                if command == key:
                    message = pastas[key]
                    break

        if not message:
            keys.extend(['keys', 'random', 'addpasta'])
            message = f'Could not find a pasta or command called {command}.'
            nearest_match = get_close_matches(command, keys)
            if nearest_match:
                message = message + f' Did you mean {nearest_match[0]}?'

        broken_string = break_string(message)
        for string in broken_string:
            body = {"bot_id": PASTABOT, "text": string}
            resp = requests.post(f'{GROUPME}/bots/post', data=body)
            if not resp.ok:
                raise ValueError(resp)

    return Response(message)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
