'''
MIT License

Copyright (c) 2021 Lee

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
import os
import discord
from discord.ext import commands
import datetime
from datetime import date
import random

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=',', intents=intents)

@bot.event
async def on_ready(): 
    bot.load_extension('cogs.Music')
    bot.load_extension('cogs.ImagesCog')
    await bot.change_presence(activity=discord.Game('sayhelp | On my feet 🤖'))

    print(f'{bot.user} has logged in.')


####/Commands/####
#kick
@bot.command(name='kick', pass_context = True) 
@commands.has_permissions(kick_members=True)
async def kick(context, member: discord.Member):
    
    channel = bot.get_channel(792824130449047552) #chat of ban/kick/mute

    await member.kick()
    await context.send('User '+ member.mention + f' has been **kicked** by {context.author} :no_entry_sign: ')

    embed = discord.Embed(title="", colour=discord.Colour(0xc80404))
    embed.add_field(name="Did shit :/", value=f'A moderator kicked user **@{member.name}** from the server :O',inline=False)
    embed.set_footer(text=f"{member.name}", icon_url=f"{member.avatar_url}")
    embed.timestamp = datetime.datetime.utcnow()

    ban = await channel.send(embed=embed) 

    emoji = '🚫'

    await ban.add_reaction(emoji)


@kick.error 
async def kick_error(ctx, error): 
    if isinstance(error, commands.MissingRequiredArgument): 
        await ctx.send('Please **specify the person** who you want to kick. Ex: ,kick @exem ')


@kick.error 
@commands.bot_has_permissions(kick_members=True)
async def kick_error(ctx, error): 
    await ctx.send(':no_entry_sign: I do not have this **permission.** Give me a big one.')


@kick.error 
@commands.has_guild_permissions(kick_members=True)
async def kick_error(ctx, error): 
    await ctx.send(':no_entry: _Invalid command_. You do not have **permission** to **kick** someone.')


#ban
@bot.command(name='ban', pass_context = True, aliases=['banuser'])
@commands.has_permissions(ban_members=True)
async def ban(context, member: discord.Member, *, reason=None): 
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


@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
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
async def ban_error(ctx, error): 
    if isinstance(error, commands.MissingRequiredArgument): 
        await ctx.send(':x: | Please **specify the person** who you want to ban. Ex: ,ban @exem')


@ban.error 
@commands.bot_has_permissions(ban_members=True)
async def ban_error(ctx, error): 
    await ctx.send(':no_entry_sign: I do not have this **permission.** Give me a big one.')


@ban.error 
@commands.has_guild_permissions(ban_members=True)
async def ban_error(ctx, error): 
    await ctx.send(':no_entry: _Invalid command_. You do not have **permission** to **ban** someone.')


@unban.error 
async def unban_error(ctx, error): 
    if isinstance(error, commands.MissingRequiredArgument): 
        await ctx.send(':x:  | Please **specify the person** who you want to unban. Ex: ,unban exem #0001')


@unban.error 
@commands.bot_has_permissions(ban_members=True)
async def unban_error(ctx, error): 
    await ctx.send(':no_entry_sign: I do not have this **permission.** Give me a big one.')


@unban.error 
@commands.has_guild_permissions(ban_members=True)
async def unban_error(ctx, error): 
    await ctx.send(':no_entry: _Invalid command_. You do not have **permission** to **unban** someone.')


#mute
@bot.command(name='mute', aliases=['m', 'muteuser'])
@commands.has_permissions(kick_members=True)
async def mute(ctx, member: discord.Member): 
    muted_role = ctx.guild.get_role(791770443605606412) #muted role id
    channel = bot.get_channel(792824130449047552) #chat of ban/kick/mute
    await member.add_roles(muted_role)
    await channel.send(member.mention + f" has **been muted** by {ctx.author}")


@bot.command(name='m_remove', aliases=['unmute'])
@commands.has_permissions(kick_members=True)
async def m_remove(ctx,member: discord.Member): 
    muted_role = ctx.guild.get_role(791770443605606412) #muted role id

    await member.remove_roles(muted_role)
    await ctx.send(f"Successfully removed **role mute** from {member.mention} by {ctx.author}. ")


@mute.error 
async def mute_error(ctx, error): 
    if isinstance(error, commands.MissingRequiredArgument): 
        await ctx.send(' :error: | Please **specify the person** who you want to mute. Ex: ,mute @exem')


@mute.error 
@commands.bot_has_permissions(kick_members=True)
async def mute_error(ctx, error): 
    await ctx.send(':no_entry_sign: I do not have this **permission.** Give me a big one.')


@mute.error 
@commands.has_guild_permissions(ban_members=True)
async def mute_error(ctx, error): 
    await ctx.send(':no_entry: _Invalid command_. You do not have **permission** to **mute someone**.')


@m_remove.error 
@commands.bot_has_permissions(kick_members=True)
async def m_remove_error(ctx, error): 
    await ctx.send(':no_entry_sign: I do not have this **permission.** Give me a big one.')


@m_remove.error 
@commands.has_guild_permissions(ban_members=True)
async def m_remove_error(ctx, error): 
    await ctx.send(':no_entry: _Invalid command_. You do not have **permission** to **remove the mute**.')


#clean chat 
@bot.command(name="clear") 
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit=amount)


@clear.error 
async def clear_error(ctx, error): 
    if isinstance(error, commands.MissingRequiredArgument): 
        await ctx.send(':x: | Please **specify an amount of messages** to delete. Ex: ,clear 10')


@clear.error 
@commands.bot_has_permissions(manage_messages=True)
async def clear_error(ctx, error): 
    await ctx.send(':no_entry_sign: I do not have this **permission.** Give me a big one.')


@clear.error 
@commands.has_guild_permissions(ban_members=True)
async def clear_error(ctx, error): 
    await ctx.send(':no_entry: _Invalid command_. You do not have **permission** to **clean the chat**.')


#Post reaction
reaction_title = ""
reactions = {}
reaction_message_id = ""

@bot.command(name="reaction_create_post")
@commands.has_permissions(manage_messages=True)
async def reaction_create_post(ctx):

    embed = discord.Embed(title="Create reaction Post", color=0x8cc542)
    embed.set_author(name="Mikasa")
    embed.add_field(name="Set Title", value=""" ,reaction_set_title \"New title\" """)     
    embed.add_field(name="Add Role", value=""" ,reaction_add_role @Role EMOJI_HERE """, inline=False)   
    embed.add_field(name="Remove Role", value=""" ,reaction_remove_role @Role""",inline=False)   
    embed.add_field(name="Send Creation Post", value=""" ,reaction_send_post""", inline=False)  

    await ctx.send(embed=embed)


@reaction_create_post.error 
@commands.has_guild_permissions(ban_members=True)
async def reaction_create_post_error(ctx, error): 
    await ctx.send(':no_entry: _Invalid command_. You do not have **permission** to **create a post.**')


@bot.command(name="reaction_set_title")
@commands.has_permissions(manage_messages=True)
async def reaction_set_title(ctx, new_title): 
    
    global reaction_title 
    reaction_title = new_title
    await ctx.send("The title for the message is now `" + reaction_title + "`!")
    await context.message.delete()


@reaction_set_title.error
async def reaction_set_title(ctx, error): 
    if isinstance(error, commands.MissingRequiredArgument): 
        await ctx.send(':exclamation: Please **specify** and set a title. Ex: ,reaction_set_title Example')


@bot.command(name="reaction_add_role")
@commands.has_permissions(manage_messages=True)
async def reaction_add_role(ctx, role: discord.Role, reaction): 
    if role != None: 
        reactions[role.name] = reaction
        await ctx.send("Role `@" + role.name + "`has been added with the emoji" + reaction)
        await ctx.message.delete()
    else: 
        await ctx.send(":x:  | Please try again!")

    print(reactions)


@reaction_add_role.error 
async def reaction_add_role(ctx, error): 
    if isinstance(error, commands.MissingRequiredArgument): 
        await ctx.send(':exclamation: Please **set** a role. Ex: ,reaction_add_role @example')


@bot.command(name="reaction_remove_role")
@commands.has_permissions(manage_roles=True)
async def reaction_remove_role(ctx, role: discord.Role): 
    if role.name in reactions: 
        del reactions[role.name] 
        await ctx.send("Role `" + role.name + "` has been added deleted!")
        await ctx.message.delete()
    else: 
        await ctx.send("That role was not added...")
    
    print(reactions)


@reaction_remove_role.error
async def reaction_remove_role(ctx, error): 
    if isinstance(error, commands.MissingRequiredArgument): 
        await ctx.send(':exclamation: Please **specify** and set the role. Ex: ,reaction_remove_role @example')


@bot.command(name="reaction_send_post")
@commands.has_permissions(manage_messages=True)
async def reaction_send_post(ctx): 
    description = "React to add the roles!\n"
    for role in reactions: 
        description += "`@" + role + "` - " + reactions[role] + "\n"

    embed = discord.Embed(title=reaction_title, description=description, color=0x8cc542)
    embed.set_author(name="MMikasa") #must use name = "" to set a author
    message = await ctx.send(embed=embed)

    global reaction_message_id 
    reaction_message_id  = str(message.id)

    for role in reactions: 
        await message.add_reaction(reactions[role])


@reaction_send_post.error 
@commands.has_guild_permissions(manage_roles=True)
async def reaction_send_post_error(ctx, error): 
    await ctx.send(':no_entry: _Invalid command_. You do not have **permission** to **create a post.**')


@bot.event
async def on_reaction_add(reaction, user):
    if not user.bot: 
        message = reaction.message 
        if str(message.id) == reaction_message_id: 
            # add roles to users 
            
            role_to_give = ""
            for role in reactions: 

                if reactions[role] == reaction.emoji: 
                    role_to_give = role

            role_for_reaction = discord.utils.get(user.guild.roles, name=role_to_give)
            await user.add_roles(role_for_reaction)


#profile picture
@bot.command(name='avatar', aliases=['Avatar','av'])
async def avatar(ctx, *, member: discord.Member=None): #set the member object to None

    if not member: #if member is no mentioned
        member = ctx.message.author #set member as the author
    show_avatar = discord.Embed(title = f'{ctx.author} - _{member.name}_',color = discord.Color.dark_blue(), icon_url=f"{member.avatar_url}")
    show_avatar.set_image(url=f'{member.avatar_url}')

    msg = await ctx.send(embed=show_avatar)
    emoji = '🤖'

    await msg.add_reaction(emoji)


#date
@bot.command(name="data", aliases=['Data'])
async def data(ctx):
    data = date.today()
    await ctx.send(f':calendar_spiral: | We are in `{data}`')


#ping
@bot.command(name="ping", aliases=['Ping'])
async def ping(ctx):
    await ctx.send(f':ping_pong: | **Pong!** \n :stopwatch: | **Gateway Ping:** `{round(bot.latency * 100)}ms` \n :satellite: | **API Ping:** `{round(bot.latency * 1000)}ms` ')


#cookie
@bot.command(pass_context=True)
async def cookie(ctx): 
    msg = await ctx.send("Here is your `cookie` :cookie:!")
    emoji = '🍪'

    await msg.add_reaction(emoji)


#modhelp 
@bot.command(name='modhelp')
@commands.has_permissions(manage_messages=True)
async def modhelp(ctx): 
    try:
        embed = discord.Embed(title=':gem: Administration Commands', description='''Hello! Use ,modhelp to know about the commands. Here is the mod commands. \n Commands found: 13 \nCategories found: 1''', color=0x00ff00)
        embed.add_field(name=":man_police_officer: - Administration commands (13)", value="`,modhelp` | `,ban` | `,unban` | `,kick` | `,mute` | `,m_remove` | `,clear` | `autorole` | `,reaction_create_post` | `reaction_set_title` | `reaction_add_role ` | `reaction_remove_role` | `reaction_send_post`", inline=False) #must use name = "" to set a author

        msg = await ctx.send(embed=embed) 
        emoji = '⁉️'

        await msg.add_reaction(emoji)
        
    except Exception as e:
        print(f'[ERROR] {e}')


@modhelp.error 
@commands.has_guild_permissions(manage_roles=True)
async def modhelp_error(ctx, error): 
    await ctx.send(':no_entry: _Invalid command_. You do not **permission.** to the **mod commands.**')


####/Events/####
#welcome message
@bot.event
async def on_member_join(member): 
    guild = bot.get_guild(790675423616696360) #id of the server
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


#sayhelp
@bot.event 
async def on_message(message):
    if message.content.startswith('sayhelp'):
        embedVar = discord.Embed(title=":gear: Commands", description=f"""Hello! Use **sayhelp** to know about the commands.
        Commands found: 26
        Categories found: 4""", color=0x00ff00)
        embedVar.add_field(name="Prefix ", value="For anything commands use the prefix **,** " ,inline=False)
        embedVar.add_field(name="About the role bot", value="It's importante that the bot must have all permissions. " ,inline=False)
        embedVar.add_field(name=":man_police_officer: - Administration commands (12)", value="`,modhelp`", inline=False)
        embedVar.add_field(name=":musical_note: - Music commands (8)", value="`,play` | `,pause` | `,resume` | `,skip` | `,now_playing` | `,queue` | `,disconnect`", inline=False)
        embedVar.add_field(name=":newspaper: - Information commands (2)", value="`,data` | `,ping` " ,inline=False)
        embedVar.add_field(name=":cherries: - Fun commands (3)", value="`,cookie` | `,avatar` | `,cat`", inline=False)

        await message.delete()
        msg = await message.channel.send(embed=embedVar)
        emoji = '❓'

        await msg.add_reaction(emoji)

    await bot.process_commands(message)
    

#error
@bot.event
async def on_command_error(ctx, error): 
    if isinstance(error, commands.CommandNotFound): 
        await ctx.send('_Invalid command_. Use **sayhelp** to learn about the commands.')
        await ctx.message.delete()

with open("src/token", "rt+") as f:
    bot.run(str(f.read()))