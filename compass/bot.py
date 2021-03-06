import discord
import asyncio
import os
import functools
import inspect
import traceback

__all__ = ['bot', 'run', 'command', 'hook', 'initialize']

bot = discord.Client()

ignored_users = []
ignore_bots = True

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    ignored_users.append(bot.user.id)
    for x in _init_hooks:
        res = x()
        if asyncio.iscoroutine(res):
            res = await res
    await bot.change_presence(game=discord.Game(name='Kill all humans'))

@bot.event
async def on_message(message):
    if message.author.id in ignored_users:
        return
    if ignore_bots and message.author.bot:
        return

    for hook in _hooks:
        res = hook(message)
        if asyncio.iscoroutine(res):
            res = await res
        if res:
            return

    if message.content.startswith('!'):
        args = message.content.split()
        cmd = args[0][1:].lower()
        resp = _invoke(cmd, *args[1:], message=message)
        if asyncio.iscoroutine(resp):
            resp = await resp
        if resp:
            await bot.send_message(message.channel, resp)

def run(token):
    return bot.run(token)

_commands = {}
_aliases = {}
_hooks = []
_init_hooks = []
def command(name, *aliases):
    def command_inner(f):
        if name in _commands:
            print('Warning: redefining '+name)
        _commands[name] = f
        for n in aliases:
            if n in _aliases:
                print('Warning: redefining '+n)
            _aliases[n] = f
        return f
    return command_inner

def hook(f):
    _hooks.append(f)
    return f

def initialize(f):
    _init_hooks.append(f)
    return f

def _shorthelp(k):
    if k in _commands:
        f = _commands[k]
    elif k in _aliases:
        f = _aliases[k]
    else:
        return "No such command."
    
    shorthelp = inspect.getdoc(f)
    if shorthelp:
        shorthelp = shorthelp.split("\n")[0]
    else:
        shorthelp = "No help for command."
    return k + " - " + shorthelp

def _usage(k):
    if k in _commands:
        f = _commands[k]
    elif k in _aliases:
        f = _aliases[k]
    else:
        return "No such command."

    doc = inspect.getdoc(f)
    if doc and len(doc.split("\n\n")) > 1:
        return doc.split("\n\n")[1]
    
    # construct it from the parameters
    p = inspect.signature(f).parameters
    u = k
    for pn in p:
        if p[pn].kind == inspect.Parameter.POSITIONAL_ONLY or p[pn].kind == inspect.Parameter.POSITIONAL_OR_KEYWORD:
            if p[pn].default == p[pn].empty:
                u += " <" + pn + ">"
            else:
                u += " [" + pn + "]"
        elif p[pn].kind == inspect.Parameter.VAR_POSITIONAL:
            u += " ..."
        else:
            break
    return u

def _invoke(k, *args, **kwargs):
    if k in _commands:
        f = _commands[k]
    elif k in _aliases:
        f = _aliases[k]
    else:
        return "I don't know what you're talking about."

    p = inspect.signature(f).parameters
    try:
        if 'message' in p:
            return f(*args, **kwargs)
        else:
            del kwargs['message']
            return f(*args, **kwargs)
    except TypeError as e:
        traceback.print_exc()
        return "Bad arguments for " + k + "\nUsage: " + _usage(k)
    except:
        traceback.print_exc()
        return "Something went wrong."

@command('help')
def help(*args, message):
    """
    Show help for a command or list commands.

    help [command]
    """
    if len(args) == 0:
        # list commands
        res = "\n".join([
            _shorthelp(k)
            for k in sorted(_commands.keys())])
        if not res:
            res = "No commands available."
        return res
    elif len(args) == 1:
        cmd = args[0].replace("!", "")
        if cmd in _commands:
            f = _commands[cmd]
        elif cmd in _aliases:
            f = _aliases[cmd]
        else:
            return "No such command."
        return _shorthelp(cmd) + "\n\n" + _usage(cmd)
    else:
        return "Bad arguments for !help."
