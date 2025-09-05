import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import webserver
import random

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='.', intents=intents)

playlist = [
    "https://youtu.be/Kza-X1x0URU?si=vZHBWEGY0LhsfOG4",
    "https://youtu.be/ZzjCiz-95Bc?si=iljAVeA-OX8RKOEd",
    "https://youtu.be/x72xck3LKtE?si=lELYYGAsoGlPUwRz",
    "https://youtu.be/pgB9LgjO4yE?si=P36x9KHL0mY7T9B7",
    "https://youtu.be/O_wwhFohA4Q?si=GKdEytd8SCiIzsjC",
    "https://youtu.be/AvMn7tjkEbQ?si=RzCwrMpbeaUNMSIa",
    "https://youtu.be/i11GrzvsB80?si=jFvUYc-HKjjM8WhG",
    "https://youtu.be/rQ7OiGMv6wU?si=_5nQH212IxhX8u3z",
    "https://youtu.be/S3E2NDOTiBY?si=xKn6egZ30ySXtO_T",
    "https://youtu.be/Sro78dNMPiA?si=zd4TqXfb1w4HVK-w",
    "https://youtu.be/6sUmOXK2JU8?si=gXzjpR8p0TmSmz29",
    "https://youtu.be/cpZQy4K5qZQ?si=kWG5C2Z1WFZLhFud",
    "https://youtu.be/uW9FkHYvriw?si=P_6Uevh7LYTSq0Dn",
    ]



secret_role = "dope mf"


@bot.event
async def on_ready():
    print(f"yo, {bot.user.name}")

@bot.event
async def on_member_join(member):
    await member.send(f"yo, {member.name}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
         return

    if "sleeptoken" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention} - never bring that shit ass band up again bruh")

    await bot.process_commands(message)

@bot.command()
async def song(ctx):
    song: object = random.choice(playlist)
    await ctx.send(f"check this sick shit out bro {song}")

@bot.command()
async def hi(ctx):
    await ctx.send(f"waddup {ctx.author.mention}")

@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is now a {secret_role}")
    else:
        await ctx.send(f"{ctx.author.mention} is not a {secret_role}")

@bot.command()
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} is not a {secret_role} anymore")
    else:
        await ctx.send(f"{ctx.author.mention} is not a {secret_role}")

@bot.command()
async def dm(ctx, *, msg):
    await ctx.author.send(f"you said {msg}")

@bot.command()
async def reply(ctx):
    await ctx.reply("THE dope bot is replying to you")

@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title="debate", description=question)
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")

@bot.command()
@commands.has_role(secret_role)
async def secret(ctx):
    await ctx.send("you a dope ass mf now bro")

@secret.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("you are not dope enough for that bro")

webserver.keep_alive()
bot.run(token, log_handler=handler, log_level=logging.DEBUG)