





#HELP COMMANDS .dnd_help <category> <name> ?

#QUICK TEMPLATE#
#async def help(self, ctx):
#    embed=discord.Embed(title="", description="")
#    embed.add_field(name="", value="", inline=False)
#    embed.add_field(name="", value="", inline=True)
#    embed.add_field(name="", value="", inline=True)
#    await ctx.send(embed=embed)

#CURRENTLY ONLY ADDING SPELLS (VERY SLOWLY), UNTILL MORE CONCRETE GUIDELINES
    
#rules

#races

async def helphuman(self, ctx):
    embed=discord.Embed(title="Human", description="Race")
    embed.add_field(name="Feature", value="+1 to every abilityscore", inline=False)
    embed.add_field(name="Feature", value="You speak the common language and can choose one additional language", inline=True)
    embed.add_field(name="Description", value="Human race is one of the most versatile and flexible options available to players. Humans possess no inherent racial traits beyond their ability score increases, but they make up for it with their adaptability and potential for customization.", inline=True)
    await ctx.send(embed=embed)

#classes (each class is a fucking massive block of text, might be easier to just research online per class *crying*. But, this stuff will go into the level up - helper if we make it, so it's not entirely meaningless in any case)

#Fighter class (next ones will be cleaner and leaner, if continued)
async def helpfighter(self, ctx):
    embed=discord.Embed(title="Fighter", description="Class")
    embed.add_field(name="Feature: Proficiencies", value="Fighters are proficient in all armor types, shields, and a wide array of weapons, granting them versatility in their equipment choices. They also gain proficiency in Strength and Constitution saving throws.", inline=False)
    embed.add_field(name="Feature: Fighting Style", value="At 1st level, Fighters choose a Fighting Style, which enhances their combat abilities.", inline=True)
    #onko mahdollista jotenkin laittaa nää stylet ton Fighting Style-fieldin alle järkevästi, eikä sillee että nää on oma fieldinsä? Vaihtoehtona voin tehdä näille samalla tavalla kun alempana tein arkkityypeille
    embed.add_field(name="Archery", value="You gain a +2 bonus to attack rolls you make with ranged weapons.", inline=True)
    embed.add_field(name="Defense", value="You gain a +1 bonus to AC (Armor Class) when wearing armor.", inline=True)
    embed.add_field(name="Dueling", value="When wielding a melee weapon in one hand and no other weapons, you gain a +2 bonus to damage rolls with that weapon.", inline=True)
    embed.add_field(name="Great Weapon Fighting", value="When you roll a 1 or 2 on a damage die for an attack you make with a two-handed or versatile melee weapon, you can reroll the die and must use the new roll.", inline=True)
    embed.add_field(name="Protection", value="When a creature you can see attacks a target other than you that is within 5 feet of you, you can use your reaction to impose disadvantage on the attack roll.", inline=True)
    #ei enää stylejä
    embed.add_field(name="Feature: Second Wind", value="At 1st level, Fighters gain the ability to recover some hit points during combat as a bonus action. This feature, called Second Wind, allows them to regain hit points equal to 1d10 plus their Fighter level, helping them endure in battles.", inline=True)
    embed.add_field(name="Feature: Action Surge", value="Starting at 2nd level, Fighters can push their limits with Action Surge. Once per short rest, they can take an additional action on top of their regular action and possible bonus actions, granting them extra attacks or the ability to use other abilities in the same turn.", inline=True)
    embed.add_field(name="Feature: Martial Archetype", value="At 3rd level, Fighters choose a Martial Archetype that defines their combat style and provides additional features.", inline=True)
    #sama kysymys näille arkkityypeille
    embed.add_field(name="Champion", value="Focuses on improved critical hits and increased durability.", inline=True)
    embed.add_field(name="Battle Master", value="Gains superiority dice to perform combat maneuvers and control the battlefield.", inline=True)
    embed.add_field(name="Eldritch Knight", value="Blends martial prowess with a limited selection of wizard spells.", inline=True)
    embed.add_field(name="Purple Dragon Knight (Banneret)", value="Inspires allies and grants bonuses in combat.", inline=True)
    embed.add_field(name="Samurai", value="Excels in social interactions and gains advantages in combat.", inline=True)
    embed.add_field(name="Cavalier", value="Specializes in mounted combat and protection.", inline=True)
    embed.add_field(name="Arcane Archer", value="Employs magical arrows and imbues their shots with arcane effects.", inline=True)
    #ei enää tyyppejä
    embed.add_field(name="Feature: Ability Score Improvement", value="At levels 4, 6, 8, 12, 14, 16 and 19, Fighters gain the Ability Score Improvement feature, allowing them to add +2 to an ability or +1 to two abilities", inline=True)
    embed.add_field(name="Feature: Extra Attacks", value="Starting at 5th level, Fighters can attack twice instead of once when they take the Attack action on their turn. This feature improves as they reach higher levels, allowing them to attack more times in a single turn.", inline=True)
    embed.add_field(name="Feature: Indomitable", value="At 9th level, Fighters gain the ability to reroll a saving throw that they fail. They can use this feature once per long rest.", inline=True)
    embed.add_field(name="Feature: Extra Attack 2", value="At 11th level, Fighters gain an extra attack when they take the Attack action, bringing their total number of attacks to three.", inline=True)
    embed.add_field(name="Feature: Martial Archetype Enhancement", value="At 15th level, Fighters gain an enhanced feature related to their chosen Martial Archetype.", inline=True)
    embed.add_field(name="Feature: Indomitable 2", value="At 17th level, Fighters' Indomitable feature improves even further. They gain an additional use of Indomitable, allowing them to reroll failed saving throws twice per long rest.", inline=True)
    embed.add_field(name="Feature: Action Surge 2", value="At 17th level, Fighters' Action Surge ability improves as well. They can now use Action Surge twice between long rests, granting them two additional actions on top of their regular action and possible bonus actions.", inline=True)
    embed.add_field(name="Feature: Superior Critical", value="At 18th level, Fighters gain the Superior Critical feature. When they score a critical hit with a weapon attack, they can roll an additional weapon damage die.", inline=True)
    embed.add_field(name="Feature: Survivor", value="At 20th level, Fighters gain the Survivor feature. Whenever they are reduced to 0 hit points but not killed outright, they can make a Constitution saving throw with a DC of 5 + the damage taken. On a success, they instead drop to 1 hit point.", inline=True)
    await ctx.send(embed=embed)

#features and traits (such as 'Nightvision' or 'Arcane recovery')

#Fighter archetype: Champion
async def helparchetypechampion(self, ctx):
    embed=discord.Embed(title="Champion", description="Fighter archetype")
    embed.add_field(name="Feature: Improved Critical", value="At 3rd level, The Champion's critical hit range expands from a natural 20 to include a roll of 19 or 20.", inline=False)
    embed.add_field(name="Feature: Remarkable Athlete", value="Starting at 7th level, add half of your proficiency bonus to st, dex and con check. Minumum str, dex or con saving throw is 14. Champion's can add half their proficiency bonus (rounded down) to any Strength, Dexterity, or Constitution check they make that doesn't already use their proficiency bonus.", inline=True)
    embed.add_field(name="Feature: Superior Critical", value="At 15th level, the Champion's critical hit range expands further to include a roll of 18, 19, or 20.", inline=True)
    embed.add_field(name="Feature: Survivor", value="Starting at 18th level, the Champion becomes an exceptional survivor on the battlefield. If they drop to 0 hit points but don't die outright, they can make a DC 5 Constitution saving throw to instead drop to 1 hit point. This saving throw can be repeated each time the Champion is reduced to 0 hit points but hasn't died outright, as long as they aren't incapacitated.", inline=True)
    await ctx.send(embed=embed)
    
#spells
async def helpmagicmissile(self, ctx):
    embed=discord.Embed(title="Magic Missile", description="Evocation Spell")
    embed.add_field(name="Casting Time", value="1 action", inline=False)
    embed.add_field(name="Range", value="120 feet", inline=True)
    embed.add_field(name="Target", value="Chosen creature within range", inline=True)
    embed.add_field(name="Components", value="V S", inline=True)
    embed.add_field(name="Duration ", value="Instant", inline=True)
    embed.add_field(name="Description", value="You create three glowing darts of magical force. Each dart hits a creature of your choice that you can see within range. A dart deals 1d4 + 1 force damage to its target. The darts all strike simultaneously, and you can direct them to hit one creature or several.", inline=True)
    embed.add_field(name="Higher Level", value="When you cast this spell using a spell slot of 2nd level or higher, the spell creates one more dart for each slot level above 1st.", inline=True)
    await ctx.send(embed=embed)
