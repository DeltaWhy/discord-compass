from compass.bot import command

@command('hello')
def hello(*args, message):
    print(message.content)
    return 'world'

@command('echo')
def echo(arg1, *args, message):
    print(message.content)
    return arg1 + ' ' + ' '.join(args)

@command('bad')
def bad(*args):
    return 'bad'

@command('bad1')
def bad1(bod):
    return 'bad1'

@command('bad2')
def bad2(message):
    return message.content
