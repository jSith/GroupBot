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


@app.route('/api/pastabot/', methods=['POST'])
def pastabot():
    # pastabot_id = 'c04d758189c5de3217830372ac'  # test
    pastabot_id = '990d346038746d572fe9d6146b'
    pastas = {
        'textbook': "Hi friends! I know that textbooks can be expensive and this place is a great way to have that cost reduced. I have quite a few online pdf books that are being used at unl in many classes. PM me with the title of the book or the ISBN and I will most likely be able to get it for you for a cheap price. Most likely 20 to 30 dollars which is a great deal when most places online would still charge over a 100 dollars for a single textbook in an online format. If you would like to know whether I have your book just PM me on messenger and I’ll see what I can do for you.",
        'me!navyseal': "What the fuck did you just fucking say to me you little Pyjak? I'll have you know I graduated top of my class in the N7 marines program, and I've been involved in numerous secret raids on the cerberus program and I have over 300 confirmed kills. I'm trained in biotic warfare and I'm the top infiltrator in the Alliance Military. You're nothing to me but just another target. I will wipe you the fuck out with biotic detonations the likes that have never been seen in this galaxy, mark my fucking words. You think you can get away with saying that shit to me on the extranet? Think again, fucker. As we speak I am contacting the shadow broker with their contact of spies all across council and non council space and your IP is being traced right now so you better prepare for the solar storm, pure blood. The storm that wipes out the pathetic little thing you call sentient life. You're fucking harvested, kid. I can be anywhere, anytime, and I can kill you in 700 different ways, and that's just with my omnitool. Not only am I extensively trained in biotic combat, but I have access to the entire arsenal of the N7 marines and the Specters and I will use them to their full extent to wipe you off the face of the citadel, you little space cow. If only you had could have known what un-goddessly retribution your little 'clever' comment was about to bring down upon you, maybe you would have held your fucking tongue. But you wouldn't, you didn't, and now you're paying the price, you god damned Bosh'tet. I will shit fury all over you. You're fucking dead, kiddo.",
        'navyseal': "What the fuck did you just fucking say about me, you little bitch? I'll have you know I graduated top of my class in the Navy Seals, and I've been involved in numerous secret raids on Al-Quaeda, and I have over 300 confirmed kills. I am trained in gorilla warfare and I'm the top sniper in the entire US armed forces. You are nothing to me but just another target. I will wipe you the fuck out with precision the likes of which has never been seen before on this Earth, mark my fucking words. You think you can get away with saying that shit to me over the Internet? Think again, fucker. As we speak I am contacting my secret network of spies across the USA and your IP is being traced right now so you better prepare for the storm, maggot. The storm that wipes out the pathetic little thing you call your life. You're fucking dead, kid. I can be anywhere, anytime, and I can kill you in over seven hundred ways, and that's just with my bare hands. Not only am I extensively trained in unarmed combat, but I have access to the entire arsenal of the United States Marine Corps and I will use it to its full extent to wipe your miserable ass off the face of the continent, you little shit. If only you could have known what unholy retribution your little 'clever' comment was about to bring down upon you, maybe you would have held your fucking tongue. But you couldn't, you didn't, and now you're paying the price, you goddamn idiot. I will shit fury all over you and you will drown in it. You're fucking dead, kiddo.",
        'weed': "DUUUUUUUUUUUUUUUUUUUUUUUUUUUUDE DUDE DUDE DUDE DUDE DUDE DUDE DUDE FUCKING WEEEEEEEEED AHAHAHAHAHAHAHA DUDE!!!!!!!!!! WEED!!!!!!!!!!!! hits bong FUCKING DUUUUUUDE that WEEED like just...................DUDE LMFFFFFAAAAAAOOOO i am so fucking HIGH on WEED right now XD WEEEEEEEEEEEEEEEEEEEEEEEEEEEED holla my DUDE!!!!!!!!!!!!!!JUST.........ROLL................MY.......................JOINT......................UP........................................AYYYYYYYYYYYYYYYYY DANK DANK DANK WEED LEGALIZE IT! LEGALIZE IT! LEGALIZE IT! ROLL EM SMOKE EM PUT EM IN A BOWL!!!!!!!!!!!!!!!!!!!! FUCKING WEEEEEEEEEEEEEEEEEED!!!!!!!!!!!!!!!!!!!!!!!!!!!! i am just FUCKING BAKED right now my DUDE!!!!!!!!!!!!!!!!!! LMAOOOOOOOOOOO RAISE YO HAND IF U TURNT AF RIGHT NOW raises both hands AYYYYYYYYYYYYYYYYY WEED DUDE WOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO I SMOKE 2 JOINTS IN DA MORNIN MON...........DUDE! WEED! HAAAAAAAAAAAA IM LIKE A FUCKIN KITE RIGHT NOW MY DUDE!!!!!!!!!!!!!!!!!!!! S O F U C K I N G H I G H O N W E E D I CANT EVEN FOCUS!!!!!!!!!!!!!!!!!!! SMOKING ONLY THE DANKEST OF HERB MY DUDE!!!!!!!!!!!!!!!!!!!!!! SOME OF THAT TRIPLE BANANA WINSTON CHURCHILL MEGA DANK GAZA GRASS YOOOOOOOOOOOOOO FUCKIN SO FUCKIN BLAZED RIGHT NOW DUUUUUUUUUUUUUUUUUUUUUUUUUUUUDDE AHAHAHAHHAA BAZINGA inhales YOOOOOOOOOOOOOOOOOOOOO cough THIS cough SHIT cough IS cough SO cough FUCKIN cough DANK my DUDE HAAHHAAAHAHAHAHAH WHY AM I EVEN LAUGHING ROTFLMAOO THIS SHIT IS NARSH BRO FUCKIN HELLA SMOKE WEED ERR DAY YEEEEEEEEEEEEEEEEEEEEEE",
        'kettlecorn': "Hey not to judge people that want to burn kettle corn at 1:15AM on a Sunday, but you should know that your vents are connected to certain wings of Kauffman and most of us can smell your burnt kettle corn. \n If you are going to burn kettle corn in your room (and I am not against you doing so) you should open a window so no one smells your burnt kettle corn. \n I know that the smell of burnt kettle corn is unpleasant to some people, and I imagine Toby would be upset if the smell of burnt kettle corn somehow made it to his room. \n Raikes students have gotten punished for burning kettle corn in the past. Burning kettle corn is a fun part of many people's college experience, but you should be careful. \n If you want advice on how to responsibly burn your kettle corn, feel free to PM me. I don't personally burn kettle corn anymore, but I think that, whoever you are, you may benefit from some advice on burning kettle corn. \n PS The burnt kettle corn is weed",
        'rickandmorty': "To be fair, you have to have a very high IQ to understand Rick and Morty. The humour is extremely subtle, and without a solid grasp of theoretical physics most of the jokes will go over a typical viewer's head. There's also Rick's nihilistic outlook, which is deftly woven into his characterisation- his personal philosophy draws heavily from Narodnaya Volya literature, for instance. The fans understand this stuff; they have the intellectual capacity to truly appreciate the depths of these jokes, to realise that they're not just funny- they say something deep about LIFE. As a consequence people who dislike Rick & Morty truly ARE idiots- of course they wouldn't appreciate, for instance, the humour in Rick's existential catchphrase 'Wubba Lubba Dub Dub,' which itself is a cryptic reference to Turgenev's Russian epic Fathers and Sons. I'm smirking right now just imagining one of those addlepated simpletons scratching their heads in confusion as Dan Harmon's genius wit unfolds itself on their television screens. What fools.. how I pity them. \n And yes, by the way, i DO have a Rick & Morty tattoo. And no, you cannot see it. It's for the ladies' eyes only- and even then they have to demonstrate that they're within 5 IQ points of my own (preferably lower) beforehand. Nothin personnel kid",
        'smarthumblehungry': "There will be times in life where people will doubt you, hate on you, and break you down. They don't believe in you and want to see you fail. These people will do everything in their power to watch you crash, burn, and fail. \n But in the true creators, entrepreneurs, and innovators nothing or no-one can stop the will to succeed, the perseverance to inspire, or the drive for greatness. Obstacles are meant to be overcome, conquered, defeated. The hate of the individuals who don't want to see you succeed will never overcome the fire in your soul that makes you wake up every day to prove the world wrong and silent the disbelievers. \n I didn't join the Jefferey S. Raikes School of Computer Science and Business to be told I could't sell vouchers for Kona Ice outside Selleck, I joined to defy the odds of the ones who told me it couldn't be done and shut me down. \n To the kids out there with a dream, don't let anyone tell you it can't be done. Don't let anyone stop you from achieving the ambitions beyond your wildest dreams. Don't let anyone tell you different; just tell them what can be done. \n I will sell those Kona Ice tickets and I will prove it can be done because I'm smart, humble, and hungry. \n - Tim Roty 2018",
        'penguinofdoom': "hi every1 im new!!!!!!! *holds up spork* my name is katy but u can call me t3h PeNgU1N oF d00m!!!!!!!! lol…as u can see im very random!!!! thats why i came here, 2 meet random ppl like me ^_^… im 13 years old (im mature 4 my age tho!!) i like 2 watch invader zim w/ my girlfreind (im bi if u dont like it deal w/it) its our favorite tv show!!! bcuz its SOOOO random!!!! shes random 2 of course but i want 2 meet more random ppl =) like they say the more the merrier!!!! lol…neways i hope 2 make alot of freinds here so give me lots of commentses!!!! \n DOOOOOMMMM!!!!!!!!!!!!!!!! <--- me bein random again ^_^ hehe…toodles!!!!! \n love and waffles, \n t3h PeNgU1N oF d00m",
        'beemovie': "According to all known laws of aviation, there is no way that a bee should be able to fly. Its wings are too small to get its fat little body off the ground. The bee, of course, flies anyways. Because bees don't care what humans think is impossible.",
        'steveharvey': "Steve Harvey: 'We asked 100 people, what is the male reproductive organ?' Contestant: 'The penis' SH: 'A WUH... HUH??' audience erupts into laughter Steve Harvey grabs onto podium to support himself laughter gets even louder SH: O lordy... one man goes into cardiac arrest and many others begin vomiting profusely from laughing too hard SH: YOU PEOPLE NEED HELP the Earth shatters and Satan rises from the underworld to claim unworthy souls the universe begins rapidly closing in on itself SH: (putting on a weary voice) Survey says... the board shows 100 for 'penis' Harvey is able to get off one more shocked look before existence as we know it comes to an end",
        'htmlparse': "You can't parse [X]HTML with regex. Because HTML can't be parsed by regex. Regex is not a tool that can be used to correctly parse HTML. As I have answered in HTML-and-regex questions here so many times before, the use of regex will not allow you to consume HTML. Regular expressions are a tool that is insufficiently sophisticated to understand the constructs employed by HTML. HTML is not a regular language and hence cannot be parsed by regular expressions. Regex queries are not equipped to break down HTML into its meaningful parts. so many times but it is not getting to me. Even enhanced irregular regular expressions as used by Perl are not up to the task of parsing HTML. You will never make me crack. HTML is a language of sufficient complexity that it cannot be parsed by regular expressions. Even Jon Skeet cannot parse HTML using regular expressions. Every time you attempt to parse HTML with regular expressions, the unholy child weeps the blood of virgins, and Russian hackers pwn your webapp. Parsing HTML with regex summons tainted souls into the realm of the living. HTML and regex go together like love, marriage, and ritual infanticide. The <center> cannot hold it is too late. The force of regex and HTML together in the same conceptual space will destroy your mind like so much watery putty. If you parse HTML with regex you are giving in to Them and their blasphemous ways which doom us all to inhuman toil for the One whose Name cannot be expressed in the Basic Multilingual Plane, he comes. HTML-plus-regexp will liquify the n​erves of the sentient whilst you observe, your psyche withering in the onslaught of horror. Rege̿̔̉x-based HTML parsers are the cancer that is killing StackOverflow it is too late it is too late we cannot be saved the trangession of a chi͡ld ensures regex will consume all living tissue (except for HTML which it cannot, as previously prophesied) dear lord help us how can anyone survive this scourge using regex to parse HTML has doomed humanity to an eternity of dread torture and security holes using regex as a tool to process HTML establishes a breach between this world and the dread realm of c͒ͪo͛ͫrrupt entities (like SGML entities, but more corrupt) a mere glimpse of the world of reg​ex parsers for HTML will ins​tantly transport a programmer's consciousness into a world of ceaseless screaming, he comes, the pestilent slithy regex-infection wil​l devour your HT​ML parser, application and existence for all time like Visual Basic only worse he comes he comes do not fi​ght he com̡e̶s, ̕h̵i​s un̨ho͞ly radiańcé destro҉ying all enli̍̈́̂̈́ghtenment, HTML tags lea͠ki̧n͘g fr̶ǫm ̡yo​͟ur eye͢s̸ ̛l̕ik͏e liq​uid pain, the song of re̸gular exp​ression parsing will exti​nguish the voices of mor​tal man from the sp​here I can see it can you see ̲͚̖͔̙î̩́t̲͎̩̱͔́̋̀ it is beautiful t​he final snuffing of the lie​s of Man ALL IS LOŚ͖̩͇̗̪̏̈́T ALL I​S LOST the pon̷y he comes he c̶̮omes he comes the ich​or permeates all MY FACE MY FACE ᵒh god no NO NOO̼O​O NΘ stop the an​*̶͑̾̾​̅ͫ͏̙̤g͇̫͛͆̾ͫ̑͆l͖͉̗̩̳̟̍ͫͥͨe̠̅s ͎a̧͈͖r̽̾̈́͒͑e n​ot rè̑ͧ̌aͨl̘̝̙̃ͤ͂̾̆ ZA̡͊͠͝LGΌ ISͮ̂҉̯͈͕̹̘̱ TO͇̹̺ͅƝ̴ȳ̳ TH̘Ë͖́̉ ͠P̯͍̭O̚​N̐Y̡ H̸̡̪̯ͨ͊̽̅̾̎Ȩ̬̩̾͛ͪ̈́̀́͘ ̶̧̨̱̹̭̯ͧ̾ͬC̷̙̲̝͖ͭ̏ͥͮ͟Oͮ͏̮̪̝͍M̲̖͊̒ͪͩͬ̚̚͜Ȇ̴̟̟͙̞ͩ͌͝S̨̥̫͎̭ͯ̿̔̀ͅ ",
        'tragedy': "Did you ever hear the tragedy of Darth Plagueis The Wise? I thought not. \n It’s not a story the Jedi would tell you. It’s a Sith legend. Darth Plagueis was a Dark Lord of the Sith, so powerful and so wise he could use the Force to influence the midichlorians to create life… \n He had such a knowledge of the dark side that he could even keep the ones he cared about from dying. The dark side of the Force is a pathway to many abilities some consider to be unnatural. He became so powerful… the only thing he was afraid of was losing his power, which eventually, of course, he did. \n Unfortunately, he taught his apprentice everything he knew, then his apprentice killed him in his sleep. Ironic. He could save others from death, but not himself.",
        'billymadison': "What you've just said is one of the most insanely idiotic things I have ever heard. At no point in your rambling, incoherent response were you even close to anything that could be considered a rational thought. Everyone in this room is now dumber for having listened to it. I award you no points, and may God have mercy on your soul.",
        'microsoft': "Our mission is to empower every person and organization on the planet to achieve more.",
        'ballmer': "DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS!",
        'google': "Our mission is to organize the world's information and make it universally accessible and useful. ̷D̷o̷n̷'̷t̷ ̷b̷e̷ ̷e̷v̷i̷l̷",
        'raikesandmorty': "To be fair, you have to have a very high IQ to get into the Raikes School of Computer Science and Management. The application prompts are extremely vague, and without a solid grasp of innovation processes, most of the applications won't even reach Anna Pressler's hands. There's also Steve's capitalist outlook, which is deftly woven into his lectures - his humble, hungry, smart philosophy draws heavily from Ideal Team Player, for instance. The students understand this stuff; they have the intellectual capacity to truly appreciate the depths of these teachings, to realize that they're not just educational- they say something deep about LIFE. \n As a consequence people who dislike the Raikes School truly ARE idiots- of course, they wouldn't appreciate, for instance, the simplicity in Steve's existential catchphrase \"At Stanford\" which itself is a cryptic reference to Alice's extensive development I'm smirking right now just imagining one of those addlepated simpletons scratching their heads in confusion as Steve Cooper's genius unfolds itself on the whiteboard. What fools... how I pity them. And yes, by the way, I DO have a Raikes School tattoo. And no, you cannot see it. It's for the ladies' eyes only- And even they have to demonstrate that they're within 1 ACT score of my own 37 (preferably lower) beforehand.", 
        'raikes': "We are intellectually curious. We lead with humility. We express gratitude. We strive for excellence. We hold each other accountable. We build resilience. We are the Raikes School, and we are better than you.",
        'spreetail': "Be relentless. Pursue challenges. Raise your bar. Act like an owner. Make Spreetail better. Practice humility. Fire your interns.", 
        'tractor': "Sometimes you ride the tractor, and other times you have to shovel cow manure.", 
        'nebraska': "Not the victory but the action. Not the goal but the game. In the humiliating loss to Ohio State the glory.", 
        'gopack': "Hail Rodgers, full of cheese, the Lord is with thee. \n Blessed art thou among QBs, and blessed is the recipient of your catches, Davante. \n Holy Rodgers, Dad of Wisconsin, play for us sinners, now and at the hour of our loss. \n Amen", 
        'doorstop': "Crosspost from KRA, but not everyone checks there, so I thought I'd post this here as well. \n Hey guys, so a lot of you have probably heard about the decision at KRA last night to ban doorstops, in addition to magneting your door. While I am personally against this decision, I wanted to at least put in a few words in defense of the decision. \n According to the 2018-2019 Kauffman housing contracts, on page 14, there is a clause which states: \n 'Any activity deemed by Housing staff to be a threat to the health and safety of residents is strictly prohibited. Prohibited activities include, but are not limited to: throwing anything out of a window, physical assault, or threat of physical altercation.' \n Based on this umbrella clause, if Christian deemed that having doorstops was a threat to our safety, then by our contract, he has a right to ban doorstops unilaterally. \n Be that as it may, if you're upset about this, like many are, I'd highly encourage you to come to the KRA meeting 2 Mondays from now (September 10th) at 9:30 to voice your opinion respectfully and courteously. If we act like whiny and entitled kids, then we'll be treated like whiny and entitled kids. If we come to the meeting and act like we just are lazy and that's why we want doorstops, then there's really not a good argument, but if we bring up the fact that doorstops build community, and encourage spontaneous interactions with our peers, then we have a pretty damn good argument on our side. \n In short, even though Christian might not change his mind about this, we still have a venue to make our voices heard in a reasonable and calm way. I'm going to be there next week, and if you feel strongly about that aspect of our community, you should be too.", 
        'lemmesmash': "This is a nice stick. I like sticks. peck peck Lemme smash, Please. No Ron, Go find Becky. You want, sum fuk? No Ron, I don't want sum fuk. I got you blue. Hey gurl, you want some tail? flick. Ugh, Ron, your tail is small. Wot? Swiggity, Swooty? You want yellow? She doesn't want yellow. Blue and yellow? No. Ron, I'm leaving! Wut? No wait lemme smash. What has my life come to? Becky thought my tail was big. Becky used to lemme smash. But Becky is smashing Ben. Ben is a hoe. peck FUCK THIS NEST, FUCK BEN. I NEED YOU BECKY. BECKY LEMME SMASH. Imma get that bitch a stick. Bitches love sticks. Wrong stick Stick, stick, stick, stick, stick, stick Need stick Got stick Becky, I got stick LEMME SMASH", 
        'truthhurts': "I just took a DNA test, turns out I'm 100% that bitch \n Even when I'm crying crazy \n Yeah, I got boy problems, that's the human in me \n Bling bling, then I solve 'em, that's the goddess in me \n You coulda had a bad bitch, non-committal \n Help you with your career just a little \n You're supposed to hold me down, but you're holding me back \n And that's the sound of me not calling you back \n Why men great 'til they gotta be great? \n Don't text me, tell it straight to my face \n Best friend sat me down in the salon chair \n Shampoo press, get you out of my hair \n Fresh photos with the bomb lighting \n New man on the Minnesota Vikings \n Truth hurts, needed something more exciting \n Bom bom bi dom bi dum bum bay", 
        'sadlaundry': "Sad laundry has been a recurring problem on 2fl this year - make sure you're writing your name on the whiteboard so someone can find you if you forget your laundry."
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
