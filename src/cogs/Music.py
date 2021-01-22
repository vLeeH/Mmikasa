import asyncio
import wavelink
import humanize
import datetime
import discord
import re
import sys
import traceback
from typing import Union
from discord.ext import commands


RURL = re.compile('https?:\/\/(?:www\.)?.+')
class MusicController:

    def __init__(self, bot, guild_id):
        self.bot = bot
        self.guild_id = guild_id
        self.channel = None

        self.next = asyncio.Event()
        self.queue = asyncio.Queue()

        self.volume = 40
        self.now_playing = None

        self.bot.loop.create_task(self.controller_loop())

    
    async def controller_loop(self):
        await self.bot.wait_until_ready()

        player = self.bot.wavelink.get_player(self.guild_id)
        await player.set_volume(self.volume)

        while True:
            if self.now_playing:
                await self.now_playing.delete()

            self.next.clear()

            song = await self.queue.get()
            await player.play(song)
            self.now_playing = await self.channel.send(f':notes: **Now Playing** :mag_right:: `{song}`', delete_after=50)

            await self.next.wait()


class Music(commands.Cog): 
    pass
    def __init__(self, bot):
        self.bot = bot
        self.controllers = {}
        
        if not hasattr(bot, 'wavelink'):
            self.bot.wavelink = wavelink.Client(bot=self.bot)

        self.bot.loop.create_task(self.start_nodes())


    async def start_nodes(self):
        await self.bot.wait_until_ready()
        node = await self.bot.wavelink.initiate_node(host='127.0.0.1',port=2333,rest_uri='http://127.0.0.1:2333',password="testing",identifier='TEST',region='us_central')

        node.set_hook(self.on_event_hook)
    

    async def on_event_hook(self, event):
        #Node hook callback.
        if isinstance(event, (wavelink.TrackEnd, wavelink.TrackException)):
            controller = self.get_controller(event.player)
            controller.next.set()


    def get_controller(self, value: Union[commands.Context, wavelink.Player]):
        if isinstance(value, commands.Context):
            gid = value.guild.id

        else:
            gid = value.guild_id

        try:
            controller = self.controllers[gid]
        except KeyError:
            controller = MusicController(self.bot, gid)
            self.controllers[gid] = controller

        return controller


    #Play command and join command☑️
    @commands.command(aliases=['p'])
    async def play(self, ctx, *, query: str, channel: discord.VoiceChannel = None):
        if not channel:
            try: 
                channel = ctx.author.voice.channel
            except AttributeError: 
                raise discord.DiscordException('_No channel to join_. Please either **specify a valid channel or join one**.')
            
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            await ctx.send(f'**Joined** `{channel.name}`  :page_facing_up: And for questions: `sayhelp`')
            try:
                await player.connect(channel.id)
                print('Join command worked.')
            except Exception as c:  
                print(f'[ERRO] {c}')
                print('Join command did not work.')

        controller = self.get_controller(ctx)
        controller.channel = ctx.channel
        
        if not RURL.match(query):
            query = f'ytsearch:{query}'

        tracks = await self.bot.wavelink.get_tracks(f'ytsearch:{query}')

        if not tracks:
            return await ctx.send('**[ERROR]**_Could not find any songs with that query_:interrobang:')

        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            await ctx.invoke(self.connect_)
        
        track = tracks[0]

        controller = self.get_controller(ctx)

        await controller.queue.put(track)
        await ctx.send(f':play_pause: **Added** `{str(track)}` to the **queue**.')
    

    #Pause command☑️.
    @commands.command(aliases=['pause'])
    async def stop(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        try: 
            if not player.is_playing:
                return await ctx.send('**[ERROR]** I am not currently playing anything!', delete_after=15)
            
            print(f'{ctx.author} used pause command')
            await ctx.send(':pause_button: **Pausing the song**', delete_after=15)
            await player.set_pause(True) #put a pause

        except Exception as e: 
            print(f'[ERROR]Pause command did not work. {e}')


    #Resume player  from a paused state command☑️.
    @commands.command() 
    async def resume(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        try: 
            if not player.paused:
                return await ctx.send('**[ERROR]** I am not currently paused!', delete_after=15)

            print(f'{ctx.author} used resume command')
            await ctx.send(':play_pause: **Resuming the player!**', delete_after=15)
            await player.set_pause(False) #stop the pause

        except Exception as e: 
            print(f'[ERROR]Resume command did not work. {e}')


    #Skip the currently playing song☑️.
    @commands.command()
    async def skip(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        try: 
            if not player.is_playing:
                return await ctx.send('**[ERROR]** I am not currently playing anything!', delete_after=15)

            print(f'{ctx.author} used skip command')
            await ctx.send(':bow_and_arrow: Skipping **the song**!', delete_after=15)
            await player.stop()
            
        except Exception as e: 
            print(f'[ERROR]Resume command did not work. {e}')


    #Retrieve the currently playing song☑️.
    @commands.command(aliases=['np', 'nowplaying'])
    async def now_playing(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        try: 
            if not player.current:
                return await ctx.send('I am not currently playing anything!')

            controller = self.get_controller(ctx)
            await controller.now_playing.delete()

            controller.now_playing = await ctx.send(f':notes: **Now playing:** `{player.current}`')        

        except Exception as e: 
            print(f'[ERROR]Now playing command did not work. {e}')

    #Queue☑️.
    @commands.command(aliases=['q'])
    async def queue(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)

        if not player.current or not controller.queue._queue:
            return await ctx.send('There are no songs currently in the queue.', delete_after=20)

        upcoming = list(itertools.islice(controller.queue._queue, 0, 5))
        try:
            fmt = '\n'.join(f'**`{str(song)}`**' for song in upcoming)
            embed = discord.Embed(title=f'Upcoming - Next {len(upcoming)}', description=fmt)

            await ctx.send(embed=embed)
        except KeyError as e: 
            print(f'[ERROR] {e}')


    #Stop and disconnect the player☑️.
    @commands.command(aliases=['dc'])
    async def disconnect(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if player.is_connected:  
            try:
                await player.disconnect()
                await ctx.send(':point_right: **Disconnected from the call.**', delete_after=20)
                print('Disconnect command worked')
                
            except KeyError as e:
                print(f'[ERROR] {e}')
        else: 
            await ctx.send(':anger: **[ERROR]** There was no controller to stop.')


def setup(bot): 
    bot.add_cog(Music(bot))
