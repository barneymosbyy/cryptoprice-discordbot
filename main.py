import discord
import os
import datetime
from pytz import timezone
from dotenv import load_dotenv
from random import randint
from pyth import get_price, get_price_change, asyncio

load_dotenv()
DISCORD_API_KEY = os.getenv('DISCORD_API_KEY')
SYMBOL = "BTC/USD"
GREEN = 0x229e8b
GREEN_COLOR_VALUE = 2268811
RED = 0xc92a35
RED_COLOR_VALUE = 13183541
DEFAULT_COLOR_VALUE = 0

status = discord.Status.online
intents = discord.Intents.default()
client = discord.Client(intents=intents, status=status)
previous_day = None


async def change_nickname():
    global previous_day
    while True:
        try:
            price = await get_price()
            cet_timezone = timezone('UTC')
            current_date = datetime.datetime.now(cet_timezone).date()
            if current_date != previous_day:
                daily_close_price = await get_price_change()
                previous_day = current_date
            change_percentage = (price - daily_close_price) / daily_close_price * 100
            for guild in client.guilds:
                try:
                    await guild.me.edit(nick=f"{price:.2f} ({change_percentage:.2f}%)")
                    all_bot_roles = [role.name for role in guild.me.roles]
                    all_bot_roles.remove("@everyone")
                    all_bot_roles.reverse()
                    # print(f"{guild.name}: {all_bot_roles}")
                    try:
                        role = discord.utils.get(guild.roles, name=all_bot_roles[1])
                    except IndexError:
                        # print(f"Missing the 2 role setup to change role color in {guild.name}")
                        continue
                    if role:
                        if change_percentage > 0 and role.color.value != GREEN_COLOR_VALUE:
                            await role.edit(color=discord.Color(GREEN))
                            # print(f"Changing to green in {guild.name}")
                        elif change_percentage < 0 and role.color.value != RED_COLOR_VALUE:
                            await role.edit(color=discord.Color(RED))
                            # print(f"Changing to red in {guild.name}")
                        elif change_percentage == 0 and role.color.value != DEFAULT_COLOR_VALUE:
                            await role.edit(color=discord.Color(0x000000))
                            # print(f"Changing to default in {guild.name}")
                    else:
                        print("Role missing")
                except discord.errors.Forbidden:
                    print("Missing permissions")
                    continue
                except discord.errors.NotFound:  # Guild not found or bot is not a member of the guild
                    print("Guild not found")
                    continue
                except OSError as e:
                    print(f"Error occurred: {e}. Retrying...")
                    await asyncio.sleep(randint(30, 90))
                except Exception as e:
                    print("Error:", e)
                    await asyncio.sleep(60)
        except ConnectionResetError:
            print("Cannot write to closing transport. Retrying...")
        await asyncio.sleep(randint(5, 10))


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    activity = discord.Activity(type=discord.ActivityType.watching, name=SYMBOL)
    await client.change_presence(activity=activity)
    client.loop.create_task(change_nickname())

client.run(DISCORD_API_KEY)
