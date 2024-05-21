import discord
from google_search import invoke_agent
from config import global_config
from google_jobs import invoke_agent_google_jobs

DISCORD_MAX_MESSAGE_LENGTH = 2000
# Define the intents your bot will use
intents = discord.Intents.default()
intents.messages = True  # Enable message events
intents.message_content = True  # Enable message content

# Create a new Discord client with the specified intents
client = discord.Client(intents=intents)


# Event to indicate that the bot has connected to Discord
@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


# Event to handle messages sent to the server
@client.event
async def on_message(message):
    # Ignore messages sent by the bot itself to prevent infinite loops
    if message.author == client.user:
        return

    # Respond to a specific command, e.g., !hello
    if message.content.startswith("!query:"):
        query = message.content.split("!query:")[1].strip()
        answer = invoke_agent(query)
    if message.content.startswith("!jobs:"):
        query = message.content.split("!jobs:")[1].strip()
        answer = invoke_agent_google_jobs(query)

    i = 0
    while i < len(answer):
        send_message = answer[i : i + DISCORD_MAX_MESSAGE_LENGTH]
        await message.channel.send(send_message)
        i += DISCORD_MAX_MESSAGE_LENGTH


# Run the bot with the token
client.run(global_config["AUTH"]["DISCORD_CLIENT_ID"])
