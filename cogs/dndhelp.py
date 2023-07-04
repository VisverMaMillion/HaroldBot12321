





#HELP COMMANDS
    
    #rules

    #races
    
    #classes

    #features and traits (such as 'Nightvision' or 'Arcane recovery')
    
    #spells
    async def helpmagicmissile(self, ctx):
        embed=discord.Embed(title="Magic Missile", description="Evocation Spell")
        embed.add_field(name="Casting Time", value="1 action", inline=False)
        embed.add_field(name="Range ", value="120 feet", inline=True)
        embed.add_field(name="Target", value="Chosen creature within range", inline=True)
        embed.add_field(name="Components", value="V S", inline=True)
        embed.add_field(name="Duration ", value="Instant", inline=True)
        embed.add_field(name="Description", value="You create three glowing darts of magical force. Each dart hits a creature of your choice that you can see within range. A dart deals 1d4 + 1 force damage to its target. The darts all strike simultaneously, and you can direct them to hit one creature or several.", inline=True)
        embed.add_field(name="Higher Level", value="When you cast this spell using a spell slot of 2nd level or higher, the spell creates one more dart for each slot level above 1st.", inline=True)
        await ctx.send(embed=embed)
