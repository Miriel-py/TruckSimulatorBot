import os
import discord
import sqlite3
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv('./.env')
BOT_TOKEN = os.getenv('BOT_TOKEN')

if __name__ == "__main__":
    con = sqlite3.connect('players.db')
    cur = con.cursor()
    
    cur.execute("SELECT * FROM players")
    registered_players = cur.fetchall()
    
    bot = commands.Bot(command_prefix="t.", help_command=None, case_insensitive = True)
    
    @bot.command()
    async def register(ctx):
        if not user_registered(ctx.author):
            registered_players.append((ctx.author.id, ctx.author.name, 0))
            cur.execute("INSERT INTO players VALUES (?,?,?,?,?)", (ctx.author.id, ctx.author.name, 0))
            con.commit()
            await ctx.channel.send("Welcome to the Truckers, {}".format(ctx.author.mention))
        else:
            await ctx.channel.send("You are already registered") 
    
    @bot.command()
    async def profile(ctx, *args):
        if user_registered(ctx.author): 
            player = get_player(ctx.author.id)
            profile = discord.Embed(title="{}'s Profile".format(player[1]))
            profile.add_field(name="Money", value=player[3])
            await ctx.channel.send(embed=profile)
        else:
            await ctx.channel.send("{} you are not registered yet! Try `t.register` to get started".format(ctx.author.mention))
    
    @bot.command()
    async def drive(ctx, *args):
        drive_embed = discord.Embed(title="{} is driving".format(ctx.author.name), description="We hope he has fun")
        await ctx.channel.send(embed=drive_embed)
    
    
    def user_registered(user):
        for player in registered_players:
            if user.id == player[0]:
                return True
        return False
    
    # TODO add player as class 
    def get_player(player_id):
        for player in registered_players:
            if player[0] == player_id:
                return player
        return None
    bot.run(BOT_TOKEN)
