import os
import time, datetime
from dotenv import load_dotenv
load_dotenv()

import discord
from discord.ext import commands
client = commands.Bot(command_prefix="!", help_command=None, case_insensitive=True)

startTime = time.time()

### Events listeners ###
@client.event
async def on_ready():
    print(f'Logged in as {client.user} --- {client.user.id}')
    print(f'Conntected to: {len(client.guilds)} guilds')


@client.event
async def on_message(message):
    if type(message.channel) is discord.DMChannel:
        return

    if "good bot" in message.content.lower():
        await message.channel.send('Thanks :heart:')

    if "bad bot" in message.content.lower():
        await message.channel.send('I\'m sorry :frowning:')

    if not message.author.bot:
        await client.process_commands(message)

###### Manual Loading/Unloading of Cogs #####
@commands.is_owner()
@client.command(hidden=True)
async def load(ctx, extension: str):
    try:
        client.load_extension(f'cogs.{extension}')
    except(AttributeError, ImportError) as e:
        print(f'{type(e).__name__}: {e}')
        await ctx.channel.send('There was an issue loading that module.')
        return
    await ctx.channel.send(f'{extension} loaded.')


@commands.is_owner()
@client.command(hidden=True)
async def unload(ctx, extension: str):
    try:
        client.unload_extension(f'cogs.{extension}')
    except(AttributeError, ImportError) as e:
        print(f'{type(e).__name__}: {e}')
        await ctx.channel.send('There was an issue unloading that module.')
        return
    await ctx.channel.send(f'{extension} unloaded.')

@commands.is_owner()
@client.command(hidden=True)
async def reload(ctx, extension: str):
    try:
        client.unload_extension(f'cogs.{extension}')
        client.load_extension(f'cogs.{extension}')
    except(AttributeError, ImportError) as e:
        print(f'{type(e).__name__}: {e}')
        await ctx.channel.send('There was an issue reloading that module.')
        return
    await ctx.channel.send(f'{extension} reloaded.')

###### Auto Load Cogs and start bot #####
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(os.getenv("BOT_TOKEN"))