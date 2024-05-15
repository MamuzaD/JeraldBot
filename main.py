from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Message, Embed
import discord.ext.commands as commands
from responses import get_response

load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")

intents: Intents = Intents.default()
intents.message_content = True  # NOQA
bot = commands.Bot(command_prefix="!!", intents=intents, case_insensitive=True)


async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('(Message was empty because intents were not enabled properly)')

    try:
        response = await get_response(user_message, bot.user.id)
        if isinstance(response, str):
            await message.channel.send(response)
        elif isinstance(response, Embed):
            await message.channel.send(embed=response)
    except Exception as e:
        print(e)


@bot.event
async def on_ready() -> None:
    print(f'{bot.user} has connected to Discord!')


@bot.event
async def on_message(message: Message) -> None:
    if message.author == bot.user:  # to prevent from responding to itself
        return

    if bot.user in message.mentions:  # must mention bot to get response
        username: str = message.author.name
        user_message: str = message.content
        channel: str = str(message.channel)

        print(f'[{channel}] - {username}: {user_message}')
        await send_message(message, user_message)


def main() -> None:
    bot.run(token=TOKEN)


if __name__ == '__main__':
    main()
