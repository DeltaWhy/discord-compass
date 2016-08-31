import discord
import asyncio
import os

bot = discord.Client()

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_message(message):
    print(message)
    if message.content.startswith('!test'):
        await bot.send_message(message.channel, 'no u')

def run(token):
    return bot.run(token)
