import discord
import responses
from discord.ext import commands
import pylast
from key import API_KEY, API_SECRET, TOKEN

network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)

async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)
        
def run_bot():
    intents = discord.Intents.default()  
    intents.message_content = True
    client = discord.Client(intents = intents)
    
    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
        
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return 

        username = str(message.author)
        user_message = str(message.content).strip()
        channel = str(message.channel)
        
        print(f'{username} said in #{channel}: {user_message}')
        
        if user_message.startswith('?'):
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        elif user_message:
            await send_message(message, user_message, is_private=False)
        else:
            await message.channel.send("Please provide a valid message.")
    
    client.run(TOKEN)