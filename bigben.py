import discord
from discord.ext import commands
from discord.ext.commands import Bot
import os
import DiscordUtils
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import time

client = commands.Bot(command_prefix = "!")
music = DiscordUtils.Music()
scheduler = AsyncIOScheduler()

@client.event
async def on_ready():
    global bot_guild
    bot_guild = client.get_guild(862783978510221343)
    print('We have logged in as {0.user}'.format(client))

@client.command(pass_context=True)
async def start(ctx):
    global pass_ctx
    pass_ctx = ctx
    await ctx.send("Starting clock")

    scheduler.add_job(clock, 'interval', hours=1, start_date='2021-07-18 06:00:00')
    scheduler.start()

async def clock():
    ctx = pass_ctx

    await discord.utils.get(ctx.guild.voice_channels, name='General').connect()

    music_player = music.create_player(ctx, ffmpeg_error_betterfix=True)
    await music_player.queue('https://www.youtube.com/watch?v=M_aj6FbwbBs', search=True)
    song = await music_player.play()
    await ctx.send('Ding Dong!')

    time.sleep(12)
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    await voice.disconnect()

client.run(##TOKEN##)
