import discord
from dotenv import load_dotenv
load_dotenv('.env.secret')
import os
import asyncio

TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client(intents=discord.Intents.all())

def run():
    client.run(TOKEN)

@discord.app_commands.command(description="help command")
@discord.app_commands.describe(value="a value")
async def help(interaction: discord.Interaction, value: str):
    print(value)
    await interaction.response.send_message("this is the help command!")

@client.event
async def on_ready():
    guilds = client.fetch_guilds()
    print(f'{client.user} is connected to the following guilds:\n'    )
    for guild in guilds:
            print(f'{guild.name}(id: {guild.id})')

if __name__ == "__main__":
    run()