import discord
from discord.ext import commands
import os
import numpy as np
import random as rd
jep1= os.path.dirname(__file__)
bot = commands.Bot(command_prefix='.')


class memes(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @bot.command()
    async def gaim(self,ctx):
        await ctx.send(jep1)
        
    @bot.command()
    async def flip(self,ctx):
        throw = rd.randint(0, 1)
        if throw == 0:
            await ctx.send('Heads!')
        else:
            await ctx.send('Tails!')



    @bot.command()  # works
    async def BombisA(self,ctx):
        await ctx.send('Getting pounded over here!')


    @bot.command(aliases=['drop', 'pls', 'droplz'])  # works
    async def dropplz(self,ctx):
        await ctx.send('But sir please!')

        
        
class komentoja(commands.Cog):
    
    def __init__(self,bot):
        self.bot = bot
    

def setup(bot):
    bot.add_cog(memes(bot))

