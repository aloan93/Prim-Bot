import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response

# Load token from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Bot Set-up
intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)

# Message functionality
async def send_message(message: Message, user_message):
    if not user_message:
        print('(Message was empty because intents were not enabled... probably)')
        return
    
    is_private = user_message[0] == '?'

    if is_private:
        user_message = user_message[1:]

    try:
        response = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    
    except Exception as e:
        print(e)

# Handling bot start-up
@client.event
async def on_ready():
    print(f'{client.user} is now running')

# Handling incoming messages
@client.event
async def on_message(message: Message):
    if message.author == client.user:
        return
    
    username = message.author
    user_message = message.content
    channel = message.channel

    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)

# Main entry point
def main():
    client.run(TOKEN)

if __name__ == '__main__':
    main()