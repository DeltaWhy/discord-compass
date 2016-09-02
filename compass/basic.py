from compass.bot import command
import random
import re

@command('ping')
def ping(*args):
    """
    Check bot status.

    ping [message]
    """
    if args:
        return ' '.join(args)
    return 'Pong!'

@command('disapprove', 'disaprove', 'dissaprove', 'dissapprove')
def disapprove(*args, message):
    """
    Express disapproval.

    disapprove [thing]
    """

    faces = ["(•_•)", "(;¬_¬)", "( ͠° ͟ʖ ͡°)", "(－‸ლ)"]

    if not message.content.startswith('!disapprove'):
        return message.author.mention + ' learn to spell! ' + random.choice(faces)
    elif len(args) > 0:
        return " ".join(args) + ": " + random.choice(faces)
    else:
        return random.choice(faces)

@command('shrug')
def shrug():
    """
    IDK.
    """
    return "¯\\_(ツ)_/¯"

@command('botsnack')
def botsnack():
    """
    Feed me!
    """
    return ":D"

@command('flip', 'coin')
def flip(*, message):
    """
    Flip a coin.
    """
    return message.author.mention + ' ' + random.choice(['heads', 'tails'])

@command('roll', 'dice')
def roll(*specs, message):
    """
    Roll dice.

    roll [[num]d<sides>[+|-<modifier>]] ...
    Ex: roll 3d4+1
    """
    if not specs:
        specs = ('d6',)
    res = []
    for spec in specs:
        m = re.match(r'(?P<num>[0-9]*)d(?P<sides>[0-9]+)'
            + r'((?P<op>[+-])(?P<mod>[0-9]+))?$', spec)
        if not m:
            raise TypeError("Bad dice specifier")
        num = int(m.group('num')) if m.group('num') else 1
        sides = int(m.group('sides'))
        op = -1 if m.group('op') == '-' else 1
        mod = int(m.group('mod')) if m.group('mod') else 0

        l = [random.randint(1, sides) for x in range(num)]
        res.append(str(sum(l) + op * mod))
    return message.author.mention + ' ' + ', '.join(res)

@command('choose', 'choice')
def choose(*args):
    """
    Evaluate alternatives.

    choose <thing> or <other-thing>
    """
    m = ' '.join(args)
    if not ' or ' in m:
        raise TypeError("No 'or' in choice")

    a, _, b = m.partition(' or ')
    return random.choice([a, b.rstrip('?')])
