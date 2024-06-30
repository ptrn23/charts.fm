import discord
import responses
from responses import get_most_recent_track
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
            
        if message.content.startswith('recent'):
            lastfm_username = 'ptrn23'
            recent_track = get_most_recent_track(lastfm_username)
            
            embed = discord.Embed(title=f'Most Recent Track for {username}',
            description=f'[{recent_track.track}]({recent_track.track.get_url()}) from *{recent_track.album}*',
            color=0xff0000)
            embed.add_field(name='Artist', value=recent_track.track.artist.name, inline=True)
            embed.add_field(name='Album', value=recent_track.album, inline=True)
            embed.add_field(name='Playback Date', value=recent_track.playback_date, inline=False)
            embed.set_thumbnail(url=recent_track.track.get_cover_image())
            
            await message.channel.send(embed=embed)
    
    client.run(TOKEN)