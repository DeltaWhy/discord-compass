from compass.bot import command, bot
import os

@command('parrot', 'party', 'partyparrot')
async def parrot(parrot='parrot', *, message):
    """
    Party like a parrot.
    """
    if os.path.exists('parrots/hd/'+parrot+'.gif'):
        await bot.send_file(message.channel, 'parrots/hd/'+parrot+'.gif')
    elif os.path.exists('parrots/hd/'+parrot+'parrot.gif'):
        await bot.send_file(message.channel, 'parrots/hd/'+parrot+'parrot.gif')
    elif os.path.exists('parrots/'+parrot+'.gif'):
        await bot.send_file(message.channel, 'parrots/'+parrot+'.gif')
    elif os.path.exists('parrots/'+parrot+'parrot.gif'):
        await bot.send_file(message.channel, 'parrots/'+parrot+'parrot.gif')
    else:
        await bot.send_message(message.channel, "Don't have that parrot. Deal with it.")
        await bot.send_file(message.channel, 'parrots/hd/dealwithitparrot.gif')
