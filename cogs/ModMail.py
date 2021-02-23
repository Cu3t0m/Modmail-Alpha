import discord
from discord.ext import commands
from datetime import datetime
import csv
import json


class ModMail(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.channels_dict = {}

        try:
            with open('channels.json') as json_file:
                self.channels_dict = json.load(json_file)
                self.bot.chosen_server_id = self.channels_dict['server id']
                self.bot.chosen_server_name =self.channels_dict['server']
                self.bot.mod_mail_channel = self.channels_dict['open']
                self.bot.resolved_mail_channel = self.channels_dict['resolved']
        except KeyError as e:
            print(e)


    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        # Check if message is in DM and message author is not a Bot
        if message.guild is None and not message.author.bot:

            # Channel must be in the cache. Otherwise use fetch_channel if channel is returned none.
            mod_channel = self.bot.get_channel(self.bot.mod_mail_channel)

            # Create and send the message as an embed to the mod mail channel
            embed = discord.Embed(title=f":e_mail: **New DM to Bot**", colour=discord.Colour.red(),
                                  timestamp=datetime.utcfromtimestamp(datetime.now().timestamp()))
            embed.add_field(name="__Message from:__", value=message.author, inline=False)
            embed.add_field(name="__Message__", value=message.content, inline=False)
            embed.add_field(name=f"How to Reply?", value=f"To Reply to this message please do `=reply {message.author.id} <message>`", inline=False)
            message = await mod_channel.send(content=f"Message by: {message.author.mention}", embed=embed)

            # Add reactions to the message
            check_mark = '\N{WHITE HEAVY CHECK MARK}'
            cross_mark = '\N{CROSS MARK}'
            await message.add_reaction(check_mark)
            await message.add_reaction(cross_mark)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        guild = self.bot.get_guild(payload.guild_id)

        # Get the mail channels
        resolved_channel = guild.get_channel(self.bot.resolved_mail_channel)
        mod_channel = guild.get_channel(self.bot.mod_mail_channel)

        # Check if the channel where reaction was made was the mod mail channel
        if payload.channel_id == self.bot.mod_mail_channel:
            message = await mod_channel.fetch_message(payload.message_id)

            # If user reacts with check mark
            if message.reactions[0].count == 2:
                if payload.emoji.name == '✅':
                    if payload.user_id != self.bot.user.id:

                        # Edit the embed to say resolved and then send.
                        embed = message.embeds[0]
                        embed.add_field(name="Status", value=f"Resolved by {payload.member.name}", inline=False)
                        msg = await resolved_channel.send(embed=embed)

                        # Add the reactions again.
                        cross_mark = '\N{CROSS MARK}'
                        await msg.add_reaction(cross_mark)

                        # Delete the old embed
                        await message.delete()

            # If user reacts with cross
            if message.reactions[1].count == 2:
                if payload.emoji.name == '❌':
                    if payload.user_id != self.bot.user.id:

                        # Edit the embed to say cancelled and then send.
                        embed = message.embeds[0]
                        embed.add_field(name="Status", value=f"Cancelled by {payload.member.name}", inline=False)
                        msg = await resolved_channel.send(embed=embed)

                        # Add the reactions again.
                        cross_mark = '\N{CROSS MARK}'
                        await msg.add_reaction(cross_mark)

                        # Delete the old message
                        await message.delete()

        # Check if the channel where reaction was made was the resolved mail channel
        if payload.channel_id == self.bot.resolved_mail_channel:
            message = await resolved_channel.fetch_message(payload.message_id)

            # If user reacts with cross mark to indicate they want to reopen a resolved or cancelled ticket
            if message.reactions[0].count == 2:
                if payload.emoji.name == '❌':
                    if payload.user_id != self.bot.user.id:

                        # Get the embed and edit to say reopened ticket
                        embed = message.embeds[0]
                        embed.add_field(name="Status", value=f"Reopened by {payload.member.name}", inline=False)
                        msg = await mod_channel.send(embed=embed)

                        # Add the reactions again.
                        check_mark = '\N{WHITE HEAVY CHECK MARK}'
                        cross_mark = '\N{CROSS MARK}'
                        await msg.add_reaction(check_mark)
                        await msg.add_reaction(cross_mark)

                        # Delete the old message.
                        await message.delete()

    @commands.command()
    async def help(self, ctx):
        """Sends the help message"""

        embed = discord.Embed(title=f"Set Up Instructions", description="This bot only contains four commands.", colour=discord.Colour.red())
        embed.add_field(name=f"Setup Command",
                        value=f"Type `=setup <incoming mail channel> <resolved queries channel>`\n"
                              f"Where incoming mail channel = the channel where you want to receive DMs\n"
                              f"And where the resolved channel is where you want resolved or cancelled "
                              f"queries to be sent", inline=False) 
        embed.add_field(name="Actions",
                        value=f"A message can be marked as completed using the :white_check_mark: reaction."
                              f"A new mail message can be cancelled using the :x: reaction. Both these reactions will send the "
                              f"mail to the resolved channel, and mark the status of it as resolved. A resolved query can be opened "
                              f"again using the :x: reaction from the resolved channel.", inline=False)
        embed.add_field(name=f"Reply Command",
                        value=f"Type `=reply <recipent id> <message>`\n"
                              f"Where recipent id = the person you want to receive the DMs\n"
                              f"And where message is the message you want sent back", inline=False)
        embed.add_field(name=f"Invite Command",
                        value=f"Type `=invite`\n"
                              f"To invite the bot to your server or Join the Support Server\n", inline=False)      
        embed.add_field(name=f"Vote Command",
                        value=f"Type `=vote`\n"
                              f"To help the bot and vote so more people can join.\n", inline=False)                                                         
        await ctx.send(embed=embed)

    @commands.command()
    async def setup(self, ctx, open_queries: discord.TextChannel, resolved_queries: discord.TextChannel):
        """Command used to setup the mod mail channels"""
        channels_dict = {'server id': ctx.message.guild.id, 'server': ctx.message.guild.name, 'open': open_queries.id, 'resolved': resolved_queries.id}
        try:
            self.bot.mod_mail_channel = open_queries.id
            self.bot.resolved_mail_channel = resolved_queries.id
            self.bot.chosen_server_id = ctx.message.guild.id
            self.bot.chosen_server_name = ctx.message.guild.name
            embed = discord.Embed(title=f"Setup Successful", description=f"Mail Channel: {open_queries.mention}\n"
                                                                         f"Resolved Channel: {resolved_queries.mention}",
                                  colour=discord.Colour.red())
            await ctx.send(embed=embed)
        
            with open('channels.json', 'w') as fp:
                json.dump(channels_dict, fp)
        except Exception as e:
            print(e)


    @setup.error
    async def setup_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title=":x: Oops!", description="You are missing a required argument.",
                                  colour=discord.Colour.red())
            embed.add_field(name=":grey_question: Syntax",
                            value=f"[=setup <open mail channel ID> <resolved mail channel ID>](https://discord.com)")
            embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url_as(format="png", size=1024))
            await ctx.send(embed=embed)

        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(title=":x: Oops!", description="One of the channels you entered does not exist.",
                                  colour=discord.Colour.red())
            embed.add_field(name=":grey_question: Syntax",
                            value=f"[=setup <open mail channel> <resolved mail channel>](https://discord.com)")
            embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url_as(format="png", size=1024))
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(ModMail(bot))

