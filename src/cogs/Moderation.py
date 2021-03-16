import discord 
from discord.ext import commands 

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(
    command_prefix=',', intents=intents)

# Cogs - class 
class Moderation(commands.Cog): 
    def __init__(self, bot): 
        self.bot = bot 

    #helpmod 
    @commands.command(aliases=['Helpmod'])
    @commands.has_permissions(kick_members=True)
    async def helpmod(self, ctx): 
        """Help for moderation commands"""
        try:
            embed = discord.Embed(title=':gem: Administration Commands', description='''Hello! Use ,helpmod to know about the commands. Here is the mod commands. \n Commands found: 13 \nCategories found: 1''', colour=discord.Colour(0xc80404))
            embed.add_field(name=":man_police_officer: - Administration commands (13)", value="`,help mod` | `,ban` | `,unban` | `,kick` | `,mute` | `,m_remove` | `,clear` | `autorole` | `,reaction_create_post` | `reaction_set_title` | `reaction_add_role ` | `reaction_remove_role` | `reaction_send_post`", inline=False) #must use name = "" to set a author

            msg = await ctx.send(embed=embed) 
            emoji = '⁉️'

            await msg.add_reaction(emoji)
            
        except Exception as e:
            print(f'[ERROR] {e}')


    @helpmod.error 
    @commands.has_guild_permissions(manage_roles=True)
    async def helpmod_error(self, ctx, error): 
        """Help error command"""
        await ctx.send(':no_entry: _Invalid command_. You do not **permission.** to the **mod commands.**')


    # Kick command
    @commands.command(pass_context = True) 
    @commands.has_permissions(kick_members=True)
    async def kick(self, context, member: discord.Member):
        
        channel = bot.get_channel(792824130449047552) #chat of ban/kick/mute

        await member.kick()
        await context.send('User '+ member.mention + f' has been **kicked** by {context.author} :no_entry_sign: ')

        embed = discord.Embed(title=""
            , colour=discord.Colour(0xc80404))
        embed.add_field(name="Did shit :/", 
            value=f'A moderator kicked user **@{member.name}** from the server :O',inline=False)
        embed.set_footer(text=f"{member.name}", 
            icon_url=f"{member.avatar_url}")

        embed.timestamp = datetime.datetime.utcnow()

        ban = await channel.send(embed=embed) 
        emoji = '🚫'
        await ban.add_reaction(emoji)


    @kick.error 
    async def kick_error(self, ctx, error): 
        if isinstance(error, commands.MissingRequiredArgument): 
            await ctx.send('Please **specify the person** who you want to kick. Ex: ,kick @exem ')


    @kick.error 
    @commands.bot_has_permissions(kick_members=True)
    async def kick_error(self, ctx, error): 
        await ctx.send(':no_entry_sign: I do not have this **permission.** Give me a big one.')


    @kick.error 
    @commands.has_guild_permissions(kick_members=True)
    async def kick_error(self, ctx, error): 
        await ctx.send(':no_entry: _Invalid command_. You do not have **permission** to **kick** someone.')


    #ban
    @commands.command(name='ban', pass_context = True, aliases=['banuser'])
    @commands.has_permissions(ban_members=True)
    async def ban(self, context, member: discord.Member, *, reason=None): 
        channel = bot.get_channel(792824130449047552) #chat of ban/kick/mute

        await member.ban(reason=reason)
        await context.send('User '+ member.mention + f' has been **banned** by {context.author}:hammer:')

        embed = discord.Embed(title="", colour=discord.Colour(0xc80404))
        embed.add_field(name="Did shit :/", value=f'A moderator **banned** user @{member.name} from the server :O',inline=False)
        embed.set_footer(text=f"{member.name}", icon_url=f"{member.avatar_url}")
        embed.timestamp = datetime.datetime.utcnow()

        ban = await channel.send(embed=embed) 

        emoji = '🚫'

        await ban.add_reaction(emoji)


    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        channel = bot.get_channel(792824130449047552) #chat of ban/kick/mute

        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users: 
            user = ban_entry.user 

            if (user.name, user.discriminator) == (member_name, member_discriminator): 
                await ctx.guild.unban(user)
                msg = await channel.send(f'The user {user.mention} has been unbanned by a moderator 👍.')

                emoji = '✅'

                await msg.add_reaction(emoji)
                return 


    @ban.error 
    async def ban_error(self, ctx, error): 
        if isinstance(error, commands.MissingRequiredArgument): 
            await ctx.send(':x: | Please **specify the person** who you want to ban. Ex: ,ban @exem')


    @ban.error 
    @commands.bot_has_permissions(ban_members=True)
    async def ban_error(self, ctx, error): 
        await ctx.send(':no_entry_sign: I do not have this **permission.** Give me a big one.')


    @ban.error 
    @commands.has_guild_permissions(ban_members=True)
    async def ban_error(self, ctx, error): 
        await ctx.send(':no_entry: _Invalid command_. You do not have **permission** to **ban** someone.')


    @unban.error 
    async def unban_error(self, ctx, error): 
        if isinstance(error, commands.MissingRequiredArgument): 
            await ctx.send(':x:  | Please **specify the person** who you want to unban. Ex: ,unban exem #0001')


    @unban.error 
    @commands.bot_has_permissions(ban_members=True)
    async def unban_error(self, ctx, error): 
        await ctx.send(':no_entry_sign: I do not have this **permission.** Give me a big one.')


    @unban.error 
    @commands.has_guild_permissions(ban_members=True)
    async def unban_error(self, ctx, error): 
        await ctx.send(':no_entry: _Invalid command_. You do not have **permission** to **unban** someone.')


    #mute
    @commands.command(name='mute', aliases=['m', 'muteuser'])
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, member: discord.Member): 
        muted_role = ctx.guild.get_role(791770443605606412) #muted role id
        channel = bot.get_channel(792824130449047552) #chat of ban/kick/mute
        await member.add_roles(muted_role)
        await channel.send(member.mention + f" has **been muted** by {ctx.author}")


    @commands.command(name='m_remove', aliases=['unmute'])
    @commands.has_permissions(kick_members=True)
    async def m_remove(self, ctx,member: discord.Member): 
        muted_role = ctx.guild.get_role(791770443605606412) #muted role id

        await member.remove_roles(muted_role)
        await ctx.send(f"Successfully removed **role mute** from {member.mention} by {ctx.author}. ")


    @mute.error 
    async def mute_error(self, ctx, error): 
        if isinstance(error, commands.MissingRequiredArgument): 
            await ctx.send(' :error: | Please **specify the person** who you want to mute. Ex: ,mute @exem')


    @mute.error 
    @commands.bot_has_permissions(kick_members=True)
    async def mute_error(self, ctx, error): 
        await ctx.send(':no_entry_sign: I do not have this **permission.** Give me a big one.')


    @mute.error 
    @commands.has_guild_permissions(ban_members=True)
    async def mute_error(self, ctx, error): 
        await ctx.send(':no_entry: _Invalid command_. You do not have **permission** to **mute someone**.')


    @m_remove.error 
    @commands.bot_has_permissions(kick_members=True)
    async def m_remove_error(self, ctx, error): 
        await ctx.send(':no_entry_sign: I do not have this **permission.** Give me a big one.')


    @m_remove.error 
    @commands.has_guild_permissions(ban_members=True)
    async def m_remove_error(self, ctx, error): 
        await ctx.send(':no_entry: _Invalid command_. You do not have **permission** to **remove the mute**.')


    #clean chat 
    @commands.command(name="clear") 
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount : int):
        await ctx.channel.purge(limit=amount)


    @clear.error 
    async def clear_error(self, ctx, error): 
        if isinstance(error, commands.MissingRequiredArgument): 
            await ctx.send(':x: | Please **specify an amount of messages** to delete. Ex: ,clear 10')


    @clear.error 
    @commands.bot_has_permissions(manage_messages=True)
    async def clear_error(self, ctx, error): 
        await ctx.send(':no_entry_sign: I do not have this **permission.** Give me a big one.')


    @clear.error 
    @commands.has_guild_permissions(ban_members=True)
    async def clear_error(self, ctx, error): 
        await ctx.send(':no_entry: _Invalid command_. You do not have **permission** to **clean the chat**.')


def setup(bot): 
    bot.add_cog(Moderation(bot))
