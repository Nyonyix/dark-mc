from os import getenv
import discord
import asyncio
import os
from discord import user
from discord import embeds
from dotenv import load_dotenv

load_dotenv()

def stripCommand(command: str) -> tuple:
    """
    Splits command into a list for better handling

    Returns 2 values:
     - Command string split into list of individual word strings (str)
     - If command has other words besides 'base_commands' (bool)
    """
    command = command.lower()
    command = command.split()
    has_extra_words = False

    if len(command) >= 2:
        has_extra_words = True
        return command, has_extra_words

    return command, has_extra_words

def compileMessage(ip: str, port: str) -> str:

    return f"```Terrafirmacraft Server is at{ip}:{port}```"

def messageFromFile(filepath: str) -> discord.Embed:
    with open(filepath, 'r') as f:
        message = f.read()

    message = message.split('%%')

    new_message = []
    for s in message:
        new_l = s.split("\n")
        new_message += new_l

    message = new_message.copy()
    new_message = []

    for s in message:
        if len(s) >= 2:
            new_message.append(s)

    message = new_message.copy()
    new_message = []

    for s in message:
        new_s = s.replace('\n', '')
        new_message.append(new_s)

    message = new_message.copy()
    del new_message

    out_message = discord.Embed(title=message[0])

    try:
        i = 1
        for y in range(len(message)):
            out_message.add_field(name=message[i], value=message[i+1])
            i += 2
    except IndexError:
        pass

    return out_message

class DiscordBot(discord.Client):
    TOKEN = os.getenv("DISCORD_TOKEN")

    def __init__(self, ip: str, port: str) -> None:
        super().__init__()
        self.ip = ip
        self.port = port

    async def on_ready(self: discord.Client) -> None:
        print(f"{self.user} has connected to Discord")

        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=" !dark-mc h"))

    async def on_message(self: discord.Client, message: discord.Message) -> None:

            # If the message is the bot it's self, It will ignore the message
            if message.author == self.user:
                return

            # Base commands are the initial commands to be used, Most of the time '!auto-name is used
            # and sub_commands are used for actual work to avoid conflicts with other bots.
            # Example: "!auto-name(base_command) register(sub_command) example(arg1) false(arg2)"

            # sub_commands are defined and checked with the message, If message does not contain a
            # sub_command, It will return an 'invalid command' response to discord.

            # The command is also converted into a arr of words for easier computation and return the command arr.
            base_commands = ["!dark-mc"]
            command, has_extra_words = stripCommand(message.content)

            # Checks if message is a base_command and has extra words afterwards
            
            try:
                print(f"\nbase_command: {base_commands[0]} : {base_commands}\ncommand: {command[0]} : {command}")
            except IndexError:
                print(f"\nbase_command: {base_commands}\ncommand: {command}\nMessage: {message.content}")

            if len(command) <= 0 or len(base_commands) <= 0:
                return

            if base_commands[0] == command[0]:
                if has_extra_words == True:
                    sub_commands = ["tfc", "TFC", "Tfc", "Terrafirmacraft", "TERRAFIRMACRAFT", "terrafirmacraft", "h", "help", "Help", "HELP"]
                    tfc_sub_commands = ["h", "help", "HELP", "Help", "IP", "ip", "Ip"]

                    # Register command check
                    if command[1] in sub_commands[0:5]:
                        if len(command) >= 3:
                            if command[2] in tfc_sub_commands[4:6]:
                                await message.channel.send(compileMessage(self.ip, self.port))
                            elif command[2] in tfc_sub_commands[0:3]:
                                await message.channel.send(embed=messageFromFile("tfc_help.txt"))                        
                        else:
                            await message.channel.send(f"```{command[1:len(command)]} are missing commands.\n Try !dark-mc h```")
                    elif command[1] in sub_commands[6:9]:
                        await message.channel.send(embed=messageFromFile("dark_mc_help.txt"))
                    else:
                        await message.channel.send(f"```{command[1:len(command)]} are invalid commands.\n Try !dark-mc h```")
                else:
                    await message.channel.send("```Invalid Command. Missing arguments\n Try !dark-mc h```")

            # Prints the received command from discord for debugging.
            print(f"Recived {message.content}")

if __name__ == "__main__":
    print(f"This is not a primary File")