from datetime import datetime
from typing import Final
import os
from dotenv import load_dotenv
from openai import OpenAI
from discord import Embed
import requests

load_dotenv()

# variables for openAI and giphy api
OPENAI_KEY: Final[str] = os.getenv("OPENAI_KEY")
openai = OpenAI(api_key=OPENAI_KEY)
GIPHY_KEY = os.getenv("GIPHY_KEY")
GIPHY_URL = "https://api.giphy.com/v1/gifs/random"


# generate openAI response for unknown messages
def generate_openai_response(user_message: str) -> str:
    augmented_message = (
        f"Mention this I am Jerald, your friendly neighborhood Viridi plant Discord Bot with the help of AI."
        f"prompt - {user_message}")
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": augmented_message}],
        max_tokens=200
    )
    return response.choices[0].message.content


# send plant related gif links
def generate_gif(search_term: str) -> str:
    params = {
        "api_key": GIPHY_KEY,
        "tag": search_term
    }

    try:
        response = requests.get(GIPHY_URL, params=params)
        data = response.json()
        gif_url = data.get("data").get("url")
        return gif_url
    except Exception as e:
        print(e)


async def get_response(user_input: str, client_id: int) -> str or Embed:
    lowered: str = user_input.lower()

    # remove @Jerald mention
    ignore = f'<@{client_id}> '
    if lowered.startswith(ignore):
        lowered = lowered[len(ignore):]

    if lowered == 'help':
        embed = Embed(title="__             Help                 __",
                      colour=0x00b0f4,
                      timestamp=datetime.now())
        embed.add_field(name="Hello I am Jerald, your friendly neighborhood Viridi plant.",
                        value="I am intended to help you with plant information or some fun gifs :)\n\nViridi plant "
                              "courtesy of Manmeet.",
                        inline=False)
        embed.add_field(name="Commands with @Jerald",
                        value="help\ngif\ngif -<search>\n<anything>",
                        inline=True)
        embed.add_field(name="Command Info",
                        value="Show this message\nShows random plant gif\nShows random search gif\nJerald's response",
                        inline=True)
        embed.set_footer(text="Jerald")

        return embed
    elif lowered == 'hello':
        return 'Hello I am Jerald, your friendly neighborhood Viridi plant.\n'
    elif 'gif -' in lowered:
        lowered = lowered.split('-')[1]  # get search term
        return generate_gif(lowered)
    elif 'gif' in lowered:
        return generate_gif("plant")
    else:
        return generate_openai_response(lowered)
