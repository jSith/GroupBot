import os
from random import choice

from flask import Flask, request, Response
import requests

app = Flask(__name__)
GROUPME = 'https://api.groupme.com/v3/bots/'
MAX_CHARS = 1000

@app.route('/api/')
def hello_world():
    return 'Hello, World!'


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


@app.route('/api/pastabot/', methods=['POST'])
def pastabot():
    pastabot_id = '990d346038746d572fe9d6146b'
    pastas = {
        'textbook': "Hi friends! I know that textbooks can be expensive and this place is a great way to have that cost reduced. I have quite a few online pdf books that are being used at unl in many classes. PM me with the title of the book or the ISBN and I will most likely be able to get it for you for a cheap price. Most likely 20 to 30 dollars which is a great deal when most places online would still charge over a 100 dollars for a single textbook in an online format. If you would like to know whether I have your book just PM me on messenger and I’ll see what I can do for you.",
        'me!navyseal': "What the fuck did you just fucking say to me you little Pyjak? I'll have you know I graduated top of my class in the N7 marines program, and I've been involved in numerous secret raids on the cerberus program and I have over 300 confirmed kills. I'm trained in biotic warfare and I'm the top infiltrator in the Alliance Military. You're nothing to me but just another target. I will wipe you the fuck out with biotic detonations the likes that have never been seen in this galaxy, mark my fucking words. You think you can get away with saying that shit to me on the extranet? Think again, fucker. As we speak I am contacting the shadow broker with their contact of spies all across council and non council space and your IP is being traced right now so you better prepare for the solar storm, pure blood. The storm that wipes out the pathetic little thing you call sentient life. You're fucking harvested, kid. I can be anywhere, anytime, and I can kill you in 700 different ways, and that's just with my omnitool. Not only am I extensively trained in biotic combat, but I have access to the entire arsenal of the N7 marines and the Specters and I will use them to their full extent to wipe you off the face of the citadel, you little space cow. If only you had could have known what un-goddessly retribution your little 'clever' comment was about to bring down upon you, maybe you would have held your fucking tongue. But you wouldn't, you didn't, and now you're paying the price, you god damned Bosh'tet. I will shit fury all over you. You're fucking dead, kiddo.",
        'navyseal': "What the fuck did you just fucking say about me, you little bitch? I'll have you know I graduated top of my class in the Navy Seals, and I've been involved in numerous secret raids on Al-Quaeda, and I have over 300 confirmed kills. I am trained in gorilla warfare and I'm the top sniper in the entire US armed forces. You are nothing to me but just another target. I will wipe you the fuck out with precision the likes of which has never been seen before on this Earth, mark my fucking words. You think you can get away with saying that shit to me over the Internet? Think again, fucker. As we speak I am contacting my secret network of spies across the USA and your IP is being traced right now so you better prepare for the storm, maggot. The storm that wipes out the pathetic little thing you call your life. You're fucking dead, kid. I can be anywhere, anytime, and I can kill you in over seven hundred ways, and that's just with my bare hands. Not only am I extensively trained in unarmed combat, but I have access to the entire arsenal of the United States Marine Corps and I will use it to its full extent to wipe your miserable ass off the face of the continent, you little shit. If only you could have known what unholy retribution your little 'clever' comment was about to bring down upon you, maybe you would have held your fucking tongue. But you couldn't, you didn't, and now you're paying the price, you goddamn idiot. I will shit fury all over you and you will drown in it. You're fucking dead, kiddo.",
        'weed': "DUUUUUUUUUUUUUUUUUUUUUUUUUUUUDE DUDE DUDE DUDE DUDE DUDE DUDE DUDE FUCKING WEEEEEEEEED AHAHAHAHAHAHAHA DUDE!!!!!!!!!! WEED!!!!!!!!!!!! hits bong FUCKING DUUUUUUDE that WEEED like just...................DUDE LMFFFFFAAAAAAOOOO i am so fucking HIGH on WEED right now XD WEEEEEEEEEEEEEEEEEEEEEEEEEEEED holla my DUDE!!!!!!!!!!!!!!JUST.........ROLL................MY.......................JOINT......................UP........................................AYYYYYYYYYYYYYYYYY DANK DANK DANK WEED LEGALIZE IT! LEGALIZE IT! LEGALIZE IT! ROLL EM SMOKE EM PUT EM IN A BOWL!!!!!!!!!!!!!!!!!!!! FUCKING WEEEEEEEEEEEEEEEEEED!!!!!!!!!!!!!!!!!!!!!!!!!!!! i am just FUCKING BAKED right now my DUDE!!!!!!!!!!!!!!!!!! LMAOOOOOOOOOOO RAISE YO HAND IF U TURNT AF RIGHT NOW raises both hands AYYYYYYYYYYYYYYYYY WEED DUDE WOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO I SMOKE 2 JOINTS IN DA MORNIN MON...........DUDE! WEED! HAAAAAAAAAAAA IM LIKE A FUCKIN KITE RIGHT NOW MY DUDE!!!!!!!!!!!!!!!!!!!! S O F U C K I N G H I G H O N W E E D I CANT EVEN FOCUS!!!!!!!!!!!!!!!!!!! SMOKING ONLY THE DANKEST OF HERB MY DUDE!!!!!!!!!!!!!!!!!!!!!! SOME OF THAT TRIPLE BANANA WINSTON CHURCHILL MEGA DANK GAZA GRASS YOOOOOOOOOOOOOO FUCKIN SO FUCKIN BLAZED RIGHT NOW DUUUUUUUUUUUUUUUUUUUUUUUUUUUUDDE AHAHAHAHHAA BAZINGA inhales YOOOOOOOOOOOOOOOOOOOOO cough THIS cough SHIT cough IS cough SO cough FUCKIN cough DANK my DUDE HAAHHAAAHAHAHAHAH WHY AM I EVEN LAUGHING ROTFLMAOO THIS SHIT IS NARSH BRO FUCKIN HELLA SMOKE WEED ERR DAY YEEEEEEEEEEEEEEEEEEEEEE",
        'kettlecorn': "Hey not to judge people that want to burn kettle corn at 1:15AM on a Sunday, but you should know that your vents are connected to certain wings of Kauffman and most of us can smell your burnt kettle corn. \n If you are going to burn kettle corn in your room (and I am not against you doing so) you should open a window so no one smells your burnt kettle corn. \n I know that the smell of burnt kettle corn is unpleasant to some people, and I imagine Toby would be upset if the smell of burnt kettle corn somehow made it to his room. \n Raikes students have gotten punished for burning kettle corn in the past. Burning kettle corn is a fun part of many people's college experience, but you should be careful. \n If you want advice on how to responsibly burn your kettle corn, feel free to PM me. I don't personally burn kettle corn anymore, but I think that, whoever you are, you may benefit from some advice on burning kettle corn. \n PS The burnt kettle corn is weed",
        'rickandmorty': "To be fair, you have to have a very high IQ to understand Rick and Morty. The humour is extremely subtle, and without a solid grasp of theoretical physics most of the jokes will go over a typical viewer's head. There's also Rick's nihilistic outlook, which is deftly woven into his characterisation- his personal philosophy draws heavily from Narodnaya Volya literature, for instance. The fans understand this stuff; they have the intellectual capacity to truly appreciate the depths of these jokes, to realise that they're not just funny- they say something deep about LIFE. As a consequence people who dislike Rick & Morty truly ARE idiots- of course they wouldn't appreciate, for instance, the humour in Rick's existential catchphrase 'Wubba Lubba Dub Dub,' which itself is a cryptic reference to Turgenev's Russian epic Fathers and Sons. I'm smirking right now just imagining one of those addlepated simpletons scratching their heads in confusion as Dan Harmon's genius wit unfolds itself on their television screens. What fools.. how I pity them. \n And yes, by the way, i DO have a Rick & Morty tattoo. And no, you cannot see it. It's for the ladies' eyes only- and even then they have to demonstrate that they're within 5 IQ points of my own (preferably lower) beforehand. Nothin personnel kid"
    }
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
