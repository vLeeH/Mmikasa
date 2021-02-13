import os 
import discord
from discord.ext import commands
import datetime
from datetime import date
import random

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(
    command_prefix=',',  help_command=None, intents=intents)

# Cogs - class 
class Commands(commands.Cog): 
    def __init__(self, bot): 
        self.bot = bot 

    @commands.command(aliases=['Help'])
    async def help(self, ctx): 
        try:
            embedVar = discord.Embed(title=":gear: Commands", description=f"""Hello! Use **sayhelp** to know about the commands.
            Commands found: 26
            Categories found: 4""", colour=discord.Colour(0xc80404))
            embedVar.add_field(name="Prefix ", value="For anything commands use the prefix **,** " ,inline=False)
            embedVar.add_field(name="About the role bot", value="It's importante that the bot must have all permissions. " ,inline=False)
            embedVar.add_field(name=":man_police_officer: - Administration commands (12)", value="`,help mod`", inline=False)
            embedVar.add_field(name=":musical_note: - Music commands (8)", value="`,help music`", inline=False)
            embedVar.add_field(name=":newspaper: - Information commands (2)", value="`,helpinfo`" ,inline=False)
            embedVar.add_field(name=":cherries: - Fun commands (5)", value="`,cookie` | `,avatar` | `,cat` | `,data` | `,ping` ", inline=False)
            embedVar.set_footer(text="Mikasa 🍒")
            embedVar.timestamp = datetime.datetime.utcnow()

            msg = await ctx.send(embed=embedVar)
            emoji = '⁉️'

            await msg.add_reaction(emoji)
        
        except: 
            await ctx.send('**Something went wrong.** Try again this commad.')


    @commands.command(aliases=['Helpmusic'])
    async def helpmusic(self, ctx): 
        try: 
            mbed = discord.Embed(title=":notes: Music commands", description="Use **,helpmusic** to see the music commands!", colour=discord.Colour(0xc80404))
            mbed.add_field(name=":musical_note: - Music commands (8)", value="`,play` | `,pause` | `,resume` | `,skip` | `,now_playing` | `,queue` | `,disconnect`", inline=False)
            
            mbed.set_footer(text="Mikasa 🍒")
            mbed.timestamp = datetime.datetime.utcnow()

            msg = await ctx.send(embed=mbed)
            emoji = '🎵'

            await msg.add_reaction(emoji)
        except Exception as e: 
            await ctx.send('Something went wrong or this command is not working!')
            print(e)



    #date
    @commands.command(aliases=['Date'])
    async def date(self, ctx):
        try:
            data = date.today()
            await ctx.send(f':calendar_spiral: | We are in `{data}`')
        except Exception as e: 
            await ctx.send('This command is not working!')
            print(e)



    #ping
    @commands.command(aliases=['Ping'])
    async def ping(self, ctx):
        try:
            await ctx.send(f':ping_pong: | **Pong!** \n :stopwatch: | **Gateway Ping:** `{round(self.bot.latency * 100)}ms` \n :satellite: | **API Ping:** `{round(self.bot.latency * 1000)}ms` ')
        except Exception as e: 
            await ctx.send('This command is not working!')
            print(e)


    #cookie
    @commands.command(pass_context=True)
    async def cookie(self, ctx): 
        msg = await ctx.send("Here is your `cookie` :cookie:!")
        emoji = '🍪'

        await msg.add_reaction(emoji)


def setup(bot):
    bot.add_cog(Commands(bot))
