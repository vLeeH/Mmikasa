import os 
import discord
from discord.ext import commands
import datetime
from datetime import date
import random

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(
    command_prefix=',', help_command=None, intents=intents)


@bot.event
async def on_ready(): 
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="🤖 | ,help "))
    print(f'{bot.user} has logged in.')


# Loading cogs.
for filename in os.listdir('./src/cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


# Reaction Posts stuff
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
    

#error
@bot.event
async def on_command_error(ctx, error): 
    if isinstance(error, commands.CommandNotFound): 
        await ctx.send('_Invalid command_. Use **sayhelp** to learn about the commands.')
        await ctx.message.delete()


with open("src/token", "rt+") as f:
    bot.run(str(f.read()))
