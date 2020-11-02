import os
import urllib.request
import bot

def getIP() -> str:
    with urllib.request.urlopen("http://checkip.dyndns.org") as data:
        ip = data.read().decode("utf-8")

    ip_index_start = int(ip.find(":") + 1)
    ip_index_end = int(ip.find("<", ip_index_start) - 1)

    return ip[ip_index_start : ip_index_end+1]

def main() -> None:

    Bot = bot.DiscordBot(getIP(), "25565")
    Bot.run(Bot.TOKEN)

if __name__ == "__main__":
    main()