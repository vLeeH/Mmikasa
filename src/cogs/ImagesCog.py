import aiohttp
import discord 
from discord.ext import commands 

bot = commands.Bot(
    command_prefix=',', help_command=None)

class Images(commands.Cog): 
    def __init__(self, bot): 
        self.bot = bot 

    @commands.command()
    async def cat(self, ctx):
        async with aiohttp.ClientSession() as cs: 
            async with cs.get("http://aws.random.cat/meow") as r: 
                data = await r.json()

                embed = discord.Embed(title="Meow", colour=discord.Colour(0xc80404))
                embed.set_image(url=data['file'])
                embed.set_footer(text="Random cats")

                msg = await ctx.send(embed=embed)
                emoji = '🐱'
                await msg.add_reaction(emoji)        


    # Get a user profile picture - Avatar
    @commands.command(aliases=['Avatar','av'])
    async def avatar(self, ctx, *, member: discord.Member=None): #set the member object to None

        if not member: #if member is no mentioned
            member = ctx.message.author #set member as the author
        
        show_avatar = discord.Embed(
            title = f'{member.name}',color = discord.Color.dark_red(), icon_url=f"{member.avatar_url}")
        show_avatar.set_image(url=f'{member.avatar_url}')

        msg = await ctx.send(embed=show_avatar)
        emoji = '🤖'

        await msg.add_reaction(emoji)


def setup(bot): 
    bot.add_cog(Images(bot))