import aiohttp
import discord 
from discord.ext import commands 

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
                embed.set_footer(text="Random cat from http://random.cat/view/691")

                await ctx.send(embed=embed)        


def setup(bot): 
    bot.add_cog(Images(bot))