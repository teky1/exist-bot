import discord
import requests
from discord.ext import commands

with open("bot_key.txt") as file:
    bot_key = file.read()

with open("hypixel_api_key.txt") as file:
    hypixel_api_key = file.read()

client = commands.Bot(command_prefix="-", help_command=None)

ign_uuid_cache = {
    "teky1": "56977856afa34a3e8e645c1a6ba1ccae"
}

exist_guild_id = "5eea86688ea8c950b6cb5f1a"

#real
role_map = {
    "verified": 872556917061455894,
    "when1": 834056868593926164,
    "hm": 834056841621143604,
    "What the duck": 834056990183391273,
    "Creators": 834056803217702913,
    "Officers": 834056803217702913,
    "Member": 834056303978479616,
    "Living": 834056303978479616
}

#boop dev
# role_map = {
#     "verified": 872558221225758762,
#     "when1": 872558303291506738,
#     "hm": 872558349542113282,
#     "What the duck": 872558393037062214,
#     "Creators": 872558427539378236,
#     "Officers": 872558427539378236,
#     "Living": 872558456131964989,
#     "Member": 872558456131964989
# }

@client.command(name="register")
async def register(ctx: commands.Context, ign):
    if ign in ign_uuid_cache:
        data = requests.get(f"https://api.hypixel.net/player?key={hypixel_api_key}&uuid={ign_uuid_cache[ign]}").json()
    else:
        data = requests.get(f"https://api.hypixel.net/player?key={hypixel_api_key}&name={ign}").json()
        if data["success"]:
            if data["player"]:
                ign_uuid_cache[ign] = data["player"]["uuid"]
            else:
                await ctx.send("I couldn't find a Minecraft account with that username :P")
                return
        else:
            print(data)
            await ctx.send("An error occurred. Please try again in a few minutes and if it still doesn't work DM <@!258048636653535234>")
            return

    try:
        discord = data["player"]["socialMedia"]["links"]["DISCORD"]
    except KeyError:
        await ctx.send("https://imgur.com/neS6wh1")
        await ctx.send("That Minecraft account does **not** have a Discord account linked to it. "
                       "To link a Discord account to your Minecraft account, log onto Hypixel and then follow the steps "
                       "shown in the GIF above. If you follow these steps and are still having trouble, DM Teky#9703")
        return

    if discord != f"{ctx.author.name}#{ctx.author.discriminator}":
        await ctx.send("https://imgur.com/neS6wh1")
        await ctx.send("That Minecraft account has a **different** Discord user linked to it. Please make sure that this is your Minecraft account "
                       "and that the Discord you have linked matches your current discord name. Steps to change your linked Discord are shown above.")
        return

    guild_data = requests.get(f"https://api.hypixel.net/guild?key={hypixel_api_key}&player={ign_uuid_cache[ign]}").json()
    await ctx.author.add_roles(ctx.guild.get_role(role_id=role_map["verified"]))
    if guild_data["guild"]:
        await ctx.author.edit(nick=f"{ign} [{guild_data['guild']['tag']}]")
    else:
        await ctx.author.edit(nick=f"{ign}")
        await ctx.send("You have now been verified!")
        return

    if guild_data["guild"]["_id"] != exist_guild_id:
        await ctx.send(f"You have now been verified as a member of {guild_data['guild']['tag']}.")
        return

    for person in guild_data["guild"]["members"]:
        if person["uuid"] == ign_uuid_cache[ign]:
            rank = person["rank"]

    await ctx.author.add_roles(ctx.guild.get_role(role_id=role_map[rank]))
    await ctx.send(f"You have now been verified as a member of **[{guild_data['guild']['tag']}]** and have been given the {rank} role.")








@register.error
async def register_error(ctx: commands.Context, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("**Correct Format:** !register <ign>")
    else:
        raise error



@client.event
async def on_ready():
    print("Ready.")

client.run(bot_key)