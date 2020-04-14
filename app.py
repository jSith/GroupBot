from base64 import b64encode
from csv import reader, writer, DictReader
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
TEST_PASTABOT = os.environ.get('TEST_PASTABOT')
RYBOT = os.environ.get('RYBOT')
KECKBOT = os.environ.get('KECKBOT')
NUKEBOT = os.environ.get('NUKEBOT')
DADBOT = os.environ.get('DADBOT')
NUKE_SENDER = os.environ.get('NUKE_SENDER')
PASTA_FILE = 'pastas.csv'
DADJOKE_FILE = 'dadjokes.csv'

app = Flask(__name__)


@app.route('/api/')
def hello_world():
    return 'Hello, World!'


@app.route('/api/dadbot/', methods=['POST'])
def dadbot():
    input_body = request.json
    text = input_body['text']
    message = ''

    if 'dadbot tell a joke' in text:
        with open(DADJOKE_FILE, 'r', encoding='utf-8') as csv:
            joke_reader = DictReader(csv)
            dad_jokes = list(joke_reader)
        message = choice(dad_jokes)['Joke']
    elif 'I am ' in text or 'I\'m ' in text:
        base = re.search('(.*)(I\'m |I am )(.*)', text).group(3)
        message = f'Hi {base}! I\'m dadbot!'
    elif 'dad' in text or 'daddy' in text:
        message = 'You rang?'

    body = {"bot_id": DADBOT, "text": message}
    resp = requests.post(f'{GROUPME}/bots/post', data=body)
    if not resp.ok:
        raise ValueError(resp)

    return Response(message)


@app.route('/api/nukebot/', methods=['POST'])
def nukebot():
    input_body = request.json
    message = input_body['text']
    sender = input_body['sender_id']

    if sender == NUKE_SENDER:
        text = ''.join([message.upper()] * 1000)
        broken_strings = break_string(text)

        for string in broken_strings:
            body = {"bot_id": NUKEBOT, "text": string}
            resp = requests.post(f'{GROUPME}/bots/post', data=body)
            if not resp.ok:
                raise ValueError(resp.content)

    return Response(message)


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


def _get_rybot_message(input_body):
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


@app.route('/api/rybot/', methods=['POST'])
def rybot():
    input_body = request.json
    message = _get_rybot_message(input_body)

    if '@RyBot' in input_body["text"]:
        body = {"bot_id": RYBOT, "text": message}
        resp = requests.post(f'{GROUPME}/bots/post', data=body)
        if not resp.ok:
            raise ValueError(resp)

    return Response(message)


def _read_pastas():
    with open(PASTA_FILE, 'r', encoding='utf-8') as csv:
        content = reader(csv)
        pastas = {}
        for row in content:
            key = row[0]
            text = row[1].replace("\\n", "\n")
            try:
                img_url = row[2]
            except IndexError:
                img_url = ''
            pastas[key] = {"text": text, "img_url": img_url}
    return pastas


def _update_git_file(new_values):
    file = requests.get(f'{GITHUB}/contents/{PASTA_FILE}',
                        headers={'Authorization': f'Bearer {GIT_TOKEN}'}).json()

    sha = file['sha']

    with open(PASTA_FILE, 'a', encoding='utf-8') as csv:
        csvwriter = writer(csv)
        csvwriter.writerow(new_values)

    with open(PASTA_FILE, 'r', encoding='utf-8') as csv:
        new_content = re.sub('\n', '\\n', csv.read())

    encoded_content = re.sub('^b\'|\'$', '', str(b64encode(new_content.encode('utf-8'))))
    msg = f"Add new pasta with key {new_values[0]}"
    body = {"message": msg, "content": encoded_content, "sha": sha}

    resp = requests.put(f'{GITHUB}/contents/{PASTA_FILE}',
                        headers={'Authorization': f'Bearer {GIT_TOKEN}'},
                        json=body)

    return resp


def _add_new_pasta(text, uid, keys, attachments):
    key = re.search('key=(.*) value=', text).group(1)
    value = re.search('value=(.*)', text).group(1)
    img = None

    new_info = [key]  # used to write to the git file -- should be either [key, value, img] or [key, value] at the end

    if key in keys:
        message = f'Could not add this pasta because there is already a pasta with the key {key}.'
        return message
    elif 'keys' in key or 'random' in key or 'addpasta' in key:
        message = f'Could not add this pasta because the key {key} is a reserved word.'
        return message

    if 'lastlikedmessage' == value:
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
                new_info.append(value)
                attachments = msg.get('attachments')
                if attachments and attachments[0]['type'] == "image":
                    img = attachments[0]["url"]
                    new_info.append(img)
    else:
        new_info.append(value)
        if attachments and attachments[0]['type'] == "image":
            img = attachments[0]["url"]
            new_info.append(img)

    if '@' in value:

        message = 'Could not add pasta because you cannot be trusted with the @ character'
        return message

    if not value and not img:
        message = f'Could not add a pasta because it was empty.'
        return message

    resp = _update_git_file(new_info)
    if not resp.ok:
        message = f'Could not add a pasta because there was an error with the Github API: {resp.content}'
    else:
        message = f'Successfully added pasta with key {key} and value {value}'

    return message


def _get_pastabot_message(command, uid, attachments):
    pastas = _read_pastas()
    keys = list(pastas.keys())
    message = ''
    img_url = ''

    if re.search('^addpasta', command):
        if not re.search('^addpasta key=(.*) value=(.*)$', command):
            message = 'Could not add pasta because the addpasta command was incorrectly formatted.'
        else:
            try:
                message = _add_new_pasta(command, uid, keys, attachments)
            except (KeyError, AttributeError) as e:
                message = f'Could not add pasta because of error {e}'
    elif command == 'keys':
        message = ', '.join(keys)
    elif command == 'random':
        message = choice(list(pastas.values()))
    else:
        for key in keys:
            if command == key:
                message = pastas[key]["text"]
                img_url = pastas[key]["img_url"]
                break

    if not message and not img_url:
        keys.extend(['keys', 'random', 'addpasta'])
        message = f'Could not find a pasta or command called {command}.'
        nearest_match = get_close_matches(command, keys)
        if nearest_match:
            message = message + f' Did you mean {nearest_match[0]}?'

    return message, img_url


@app.route('/api/pastabot/', methods=['POST'])
def pastabot():
    input_body = request.json

    if request.args.get('test'):
        bot_id = TEST_PASTABOT
    else:
        bot_id = PASTABOT

    text = input_body["text"]
    uid = input_body["sender_id"]
    sender_type = input_body["sender_type"]
    attachments = input_body.get('attachments')

    if sender_type == "bot":
        return Response()

    pattern = re.search('@pastabot (.*)$', text)

    if not pattern:
        return Response()

    command = pattern.group(1)
    message, img_url = _get_pastabot_message(command, uid, attachments)

    broken_string = break_string(message)
    for string in broken_string:
        body = {"bot_id": bot_id, "text": string}
        resp = requests.post(f'{GROUPME}/bots/post', data=body)
        if not resp.ok:
            raise ValueError(resp)

    if img_url:
        body = {"bot_id": bot_id, "picture_url": img_url}
        resp = requests.post(f'{GROUPME}/bots/post', data=body)
        if not resp.ok:
            raise ValueError(resp)

    return Response(message)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
