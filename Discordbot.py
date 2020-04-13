import discord 
from discord.ext import commands 
from discord.utils import get
import youtube_dl
import random as rd


client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    print('Need backup!')    

@client.command(pass_context=True)
async def backup(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    
@client.command(pass_context=True)
async def noob(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
    else:
        return
        
@client.command(pass_context=True)
async def play(ctx):
    channel = ctx.message.author.voice.channel
    url = ctx.message.content
    url = url.strip('.play')
    voice = await channel.connect()
    
 #   ydl_opts = {
  #      'format': 'bestaudio/best',
   #     'postprocessors': [{
    #        'key'}]
        
        
        
     #   }
    
    
    player = await voice.create_ytdl_player(url)
    player.start()

    

@client.command()
async def lag(ctx):
    await ctx.send(f'{round(client.latency * 100)} ms ')
    
    
@client.command()
async def BombisA(ctx):
    await ctx.send('*Dies at B*')
    
@client.command(aliases =  ['KYs','kys','Kys','KyS'])
async def KYS(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    await ctx.send('AAAARGH!')
    if voice and voice.is_connected():
        await voice.disconnect()
        exit()
    else:
        exit()
        
@client.command()
async def die(ctx):
    exit()
    
    
    
client.run('Njk5MjE0ODgzMDQzOTM0Mjcw.XpRJyQ.sc6BwKjQIB6hARaAIipP-2QVAxA')


