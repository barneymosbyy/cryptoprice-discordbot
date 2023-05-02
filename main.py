import discord
from pyth import get_price, asyncio

TOKEN = "YOUR DISCORD TOKEN"
status = discord.Status.online
intents = discord.Intents.default()
client = discord.Client(intents=intents, status=status)


async def update_activity():
    while True:
        price = await get_price()
        activity = discord.Activity(type=discord.ActivityType.watching, name=f"${price:.2f}")
        await client.change_presence(activity=activity)
        await asyncio.sleep(5)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    client.loop.create_task(update_activity())

client.run(TOKEN)
