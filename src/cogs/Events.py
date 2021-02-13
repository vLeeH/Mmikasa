import discord 
from discord.ext import commands 

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(
    command_prefix=',', help_command=None, intents=intents)

# Cogs - class 
class Events(commands.Cog): 
    def __init__(self, bot): 
        self.bot = bot 

    # Welcome message
    @commands.Cog.listener()
    async def on_member_join(self, member): 
        guild = self.get_guild(790675423616696360) #id of the server
        channel = guild.get_channel(792102494498586684) #channel (welcome)

        try: 
            await channel.send(f'{member.mention}')
            embed = discord.Embed(title=":wave: Welcome to the server!", description=f"{member.mention}, i hope you enjoy the server and make new friends!", colour=discord.Colour(0x2a2a2c))
            embed.set_thumbnail(url=f"{member.avatar_url}")
            embed.set_author(name=f"{member.name}", icon_url=f"{member.avatar_url}")
            embed.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()

            await channel.send(embed=embed) 
            print(f'{member} joined in the server.')

        except Exception as e: 
            print(f'[ERROR]Welcome message did not work. {e}')


        try: 
            #message on dm
            mbed = discord.Embed(title=f"Welcome to the **{guild.name}** server :partying_face:!", description=f"{member.name} here is the invite of the server https://discord.gg/jMeHAAzB", colour=discord.Colour(0x2a2a2c))
            mbed.set_author(name=f"{member.name}", icon_url=f"{member.avatar_url}")
            mbed.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
            mbed.timestamp = datetime.datetime.utcnow()
            await member.send(embed=mbed) #welcome the member on the dm 
            
            #autorole
            role = member.guild.get_role(791424849976229899) #id of role
            await member.add_roles(role)
            print(f'{member} ganhou @{role}')

        except Exception as e: 
            print(f'[ERROR]Autorole did not work. {e}')


def setup(bot): 
    bot.add_cog(Events(bot))