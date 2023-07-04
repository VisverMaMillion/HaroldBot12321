from discord.ext import commands, tasks
from discord import app_commands
import numpy.random

skilltable = {"acrobatics":0, "animal":1, "arcana":2, "athletics":3, "deception":4 , "history":5, "insight":6, "intimidation":7, "investigation":8, "medicine":9, "nature":10, "perception":11, "performance":12 , "persuasion":13, "religion":14, "thief":15, "stealth":16, "survival":17}
savetable = {"armor":0, "str":1, "dex":2, "con":3, "int":4, "wis":5, "cha":6}
abitable = {"str":0, "dex":1, "con":2, "int":3, "wis":4, "cha":5}
rolltable = {"save":"saves","ab":"abilityscore", "skill":"skills"}


features = {"Cunning_action":(("save", "str", 1), ("abilityscore", "int", 3)),

}

class DND(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client
        self.chars = {'Daira': {'saves': [10, -1, 1, 1, 5, 4, 1], 'abilityscore': [8, 12, 12, 16, 15, 13], 'weapons': {}, 'skills': [1, 2, 5, -1, 1, 5, 4, 1, 3, 2, 3, 2, 1, 3, 3, 1, 1, 2],"weapon":None, "hp":0}}
        self.npcs = {}
        self.money = 0

    @app_commands.command(description="Create character with unique name")
    async def dnd_createchar(self, ctx, name):
        self.chars.update({name:{"saves":[], "abilityscore":[], "weapons":{}, "skills":[], "maxhp":0, "hp":0, "weapon":None}})
        await ctx.send(f'Created character {name}!')


    @app_commands.command(description="Set character save stats. Order:armor, str, dex, con, int, wis, cha")
    async def dnd_setsaves(self, ctx, char, *dum):
        l = list(map(int, list(dum)))
        self.chars[char]["saves"] = l
        await ctx.send(self.chars)

    @app_commands.command(description="Set character abilityscore stats. Order:str, dex, con, int, wis, cha")
    async def dnd_setas(self, ctx, char, *dum):
        l = list(map(int, list(dum)))
        self.chars[char]["abilityscore"] = l
        await ctx.send(self.chars)

    @app_commands.command(description="set character skill stats. Order: Dnd sheet top to bottom")
    async def dnd_setskills(self, ctx, char, *dum):
        l = list(map(int, list(dum)))
        self.chars[char]["skills"] = l
        await ctx.send(self.chars)

    #add weapon
    @app_commands.command(description="Give character a weapon. Usage: char weaponname, attackbonus, used dice, damagetypebonus")
    async def dnd_addweapon(self, ctx, char,name, abonus, dice, dtype):
        parse = dice.split("d")
        self.chars[char]["weapons"].update({name:(int(abonus),int(parse[0]), int(parse[1]),int(dtype))})
        await ctx.send(self.chars)

    @app_commands.command(description="Equip weapon for character.")
    async def dnd_weapon(self, ctx, char, name):
        try:
            self.chars[char]["weapon"] = self.chars[char]["weapons"][name]
            await ctx.send(f"{char} switched to {name}")
        except KeyError:
            await ctx.send(f"{char} does not have a {name}")


    @app_commands.command(description="Update one save stat.")
    async def dnd_updatesave(self, ctx, char, index, num):
        index = savetable[index]
        self.chars[char]["saves"][int(index)] = int(num)
        await ctx.send(self.chars)

    @app_commands.command(description="Update one abilityscore stat")
    async def dnd_updateas(self, ctx, char, index, num):
        index = abitable[index]
        self.chars[char]["abilityscore"][int(index)] = int(num)
        await ctx.send(self.chars)

    @app_commands.command(description="Update one skill stat")
    async def dnd_updateskill(self, ctx, char, index, num):
        am = skilltable[index]
        self.chars[char]["skills"][am] = int(num)
        await ctx.send(f"Updated {char} {index} to  {num}")


    @app_commands.command(description="Set character max hp, also heal to full.")
    async def dnd_setmaxhp(self, ctx, char, hp):
        self.chars[char]["maxhp"] = int(hp)
        self.chars[char]["hp"] = int(hp)

    @app_commands.command(description="Add/remove health from character.")
    async def dnd_addhp(self, ctx, char, hp):
        dum = self.chars[char]["hp"]
        maxhp = self.chars[char]["maxhp"]
        add = int(hp) +dum
        if add > maxhp:
            self.chars[char]["hp"] = maxhp
        else:
            self.chars[char]["hp"] = add
        currenthp = self.chars[char]["hp"]
        await ctx.send(f"{char} has now {currenthp} hp")

    @app_commands.command(description="Add/remove party money.")
    async def dnd_money(self, ctx, amount):
        self.money += int(amount)
        await ctx.send(f"Balance:{self.money}")

    @app_commands.command(description="Show how much money the party has.")
    async def dnd_balance(self, ctx):
        await ctx.send(f"Balance:{self.money}")

    @app_commands.command(description="Do a skill check. Order: char, skilltype, skill")
    async def dnd_check(self, ctx, char, t, s):
        ct = rolltable[t]
        if ct == "skills":
            index = int(skilltable[s])
            modif = self.chars[char][ct][index]
        elif ct == "saves":
            index = int(savetable[s])
            modif = self.chars[char][ct][index]
        else:
            index = int(abitable[s])
            modif = int((self.chars[char][ct][index]-10)/2)

        index = int()
        #modif = self.chars[char][ct][index]
        dice = numpy.random.randint(1,21)
        await ctx.send(f"{dice} +{modif} = {dice+modif}")


    @app_commands.command(description="Roll if character hit landed.")
    async def dnd_hitroll(self, ctx, char):
        weapon = self.chars[char]["weapon"]
        dice = numpy.random.randint(1,21)
        await ctx.send(f"{dice} +{weapon[0]} ={dice +weapon[0]}")

    @app_commands.command(description="Roll damage done by character.")
    async def dnd_dmgroll(self, ctx, char):
        weapon = self.chars[char]["weapon"]
        dicesum = 0
        for i in range(weapon[1]):
            await ctx.send("omega")
            dicesum += numpy.random.randint(1,weapon[2]) + weapon[3]
        await ctx.send(dicesum)
        

    @app_commands.command(description="Roll given dice and add optional bonus. Example: 1d20 3")
    async def dnd_dice(self, ctx, help, rest=0):
        parse = help.split("d")
        dice = numpy.random.randint(1,parse[1])
        await ctx.send(f"Rolled {dice+int(rest)}")

    @commands.command()
    async def dndprint(self, ctx):
        print(self.chars)



#class createchar():
    
#    def setstats(ctx):
#        stats = from message
#        charaterslist[nimi] = stats

   
#    set saves(armor, strength, dex, constitution, intelligence, wisdom, charisma)
#    set abilityscore(strength, dex, constitution, intelligence, wisdom, charisma)
#    set weapon(dmg, dmg_type, hit)

#     set skills(acro, animal, arcana, atheltic, decep, histo, insict, intimid, invest, medic, nat, percep, perfor, percu, relig, thiev, steath, surviv)

#class creatnpc():
#    set attac 

#int((abilitys -10)/2) +lisäys




async def setup(client):
    await client.add_cog(DND(client))
