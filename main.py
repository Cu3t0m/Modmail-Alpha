import discord
from discord.ext import commands
from dotenv import load_dotenv
from keep_alive import keep_alive
import os
import csv

load_dotenv()

prefix = ("=")
token = ("YoURt0KenGoE5hEreYoURt0KenGoE5hEreYoURt0KenGoE5hEre")

client = commands.Bot(command_prefix=prefix, case_insensitive=True, help_command=None)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    activity = discord.Activity(name='my DMs', type=discord.ActivityType.watching)
    await client.change_presence(activity=activity)

@client.event
async def on_message(message):
    # If the message sender is the bot itself, stop to prevent endless loop.
    if message.author.id == client.user.id:
        return

    # Reacting to bot being mentioned
    if client.user in message.mentions:
        embed=discord.Embed(title="Current prefix: `=`", description=None, color=discord.Colour.red())
        await message.channel.send(embed=embed)

    # Getting current prefix
    if message.content.startswith("prefix"):
        await message.channel.send(f"Current prefix: `=`")

    # Make sure to process commands if no on_message event was triggered, else commands won't work.
    # This only applies to the @client.event variant (because it overwrites the default one)
    await client.process_commands(message)

@client.command()
async def vote(ctx):
      embed=discord.Embed(title="Vote for Modmail", colour=discord.Colour.red())
      embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/KhrNawdHX7OC-ehRHH4GNnAkEJN8IhdEv2z9s9MnhdM/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/798480731344470077/67daf86b0106e9728cf516916427d361.webp?width=500&height=500")
      embed.add_field(name="__top.gg__", value="[Vote Now!](https://top.gg/bot/798480731344470077/vote)", inline=False)
      embed.add_field(name="__discordbotlist.com__", value="[Vote Now!](https://discordbotlist.com/bots/modmail-2403/upvote)", inline=True)
      await ctx.send(embed=embed)

@client.command()
async def invite(ctx):
      embed=discord.Embed(title="Invite The Bot or Join our Support Server", colour=discord.Colour.red())
      embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/KhrNawdHX7OC-ehRHH4GNnAkEJN8IhdEv2z9s9MnhdM/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/798480731344470077/67daf86b0106e9728cf516916427d361.webp?width=500&height=500")
      embed.add_field(name="__Invite__", value="[Join Now!](https://discord.com/oauth2/authorize?client_id=798480731344470077&permissions=8&scope=bot)", inline=False)
      embed.add_field(name="__Support Server__", value="[Join Now!](https://discord.gg/jcKUHR8pV8)", inline=True)
      await ctx.send(embed=embed)

@client.command()
async def reply(ctx, member: discord.Member, *, message: str):
    try:
        # Send the message by calling the .send method on the member object
        await member.send(f"`Staff` 🛠️: {message}")

    # If user is not in guild or has enabled privacy settings
    except discord.Forbidden:
        await ctx.send(f"Failed to send message to {member}.")

extensions = ['cogs.ModMail']

if __name__ == '__main__':
    for ext in extensions:
        client.load_extension(ext)




keep_alive()
client.run(token)
