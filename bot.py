import discord
import requests
import random
from discord.ext import commands

with open("bot_key.txt") as file:
    bot_key = file.read()

client = commands.Bot(command_prefix="-", help_command=None)

def formatName(num, name):
    # remove old num
    for i,x in enumerate(name):
        if x != " " and not x.isnumeric():
            name = name[i:]
            break

    return f"{num} {name}"

@client.command(name="paranoia")
async def paranoia(ctx: commands.Context):
    # check if persons in a vc

    if ctx.message.author.voice is None:
        await ctx.send("You need to be in a VC to use this command")
        return

    # get whos in vc with them

    vc = ctx.message.author.voice.channel
    print(vc.name)
    member_ids = list(vc.voice_states.keys())
    members = await ctx.message.guild.query_members(limit=len(member_ids), user_ids=member_ids)

    # assign them all random number
    random.shuffle(members)

    # add number to everyones name but if no perms then ping and tell them to do themselves
    await ctx.send("Generating and assigning a random order...")
    for i,member in enumerate(members):
        new_name = formatName(i+1, member.display_name)
        try:
            await member.edit(nick=new_name)
        except discord.errors.Forbidden:
            await ctx.send(f"<@!{member.id}> I don't have perms to change your nick. "
                           f"Please put a **{i+1}** in front of your name.")
    await ctx.send("Done.")

    return

@client.event
async def on_ready():
    print("Ready.")

client.run(bot_key)