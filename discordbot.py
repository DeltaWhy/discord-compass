import discord
import asyncio

client = discord.Client()

@client.event
@asyncio.coroutine
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
@asyncio.coroutine
def on_message(message):
    print(message)
    if message.content.startswith('!test'):
        yield from client.send_message(message.channel, 'no u')

client.run('MjE3NDI1ODIwNjY5NTc1MTY4.Cp0dYg.zqMwAOplMqeLDUeYIDChd5MPV64')
