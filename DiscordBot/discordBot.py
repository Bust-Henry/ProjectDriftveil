import discord
import os
from dotenv import load_dotenv
load_dotenv()
load_dotenv(os.environ.get("discordSecret"))
import requests
from discord.ui import Select, View
from discord import app_commands

REQUESTS_TIMEOUT = 5
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client(intents=discord.Intents.all())
tree = discord.app_commands.CommandTree(client)

@tree.command(name="menue", description="syncs the slash commands")
async def menue(interaction:discord.Interaction):
    response = requests.get("http://127.0.0.1:8080/", timeout=10)
    options = []
    for command in response.json().keys():
            command = command.split("/")[1]        
            options.append(discord.SelectOption(label=command, description=""))   
    select = Select(
        placeholder="Choose a command!",
        options=options
    )
    async def select_callback(interaction:discord.Interaction):
        if select.values[0] == "status":
            #response = requests.get(f"http://127.0.0.1:8080/{select.values[0]}", timeout=10)
            await interaction.response.send_message("this command is not implemented yet")
        else:
            response = requests.get(f"http://127.0.0.1:8080/{select.values[0]}", timeout=10)
            with open("temp.json", "w") as jsonfile:
                import json
                json.dump(response.json(), jsonfile, indent=4)
            await interaction.channel.send(file=discord.File("temp.json"))
        #await interaction.response.send_message(response.json())
    select.callback = select_callback
    view = View()
    view.add_item(select)
    await interaction.response.send_message(view=view)

@tree.command(name="sync", description="syncs the slash commands")
async def sync(interaction):
    global tree
    await tree.snyc()

@client.event
async def on_ready():
    global tree
    await tree.sync()
    guilds = client.fetch_guilds()
    print(f'{client.user} is connected to the following guilds:\n'    )
    async for guild in guilds:
            print(f'{guild.name}(id: {guild.id})')

def run():
    client.run(TOKEN)

if __name__ == "__main__":
    run()