import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import webserver

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='.', intents=intents)

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