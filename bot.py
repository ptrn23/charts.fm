import discord
import responses
import pylast

from responses import get_most_recent_track
from color_pick import get_dominant_color, rgb_to_hex
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
            cover_image_url = recent_track.track.get_cover_image()
            
            embed = discord.Embed(
            title=f'{recent_track.track}',
            color=0xff0000)
            embed.add_field(name='Artist', value=recent_track.track.artist.name, inline=True)
            embed.add_field(name='Album', value=recent_track.album, inline=True)
            embed.add_field(name='Playback Date', value=recent_track.playback_date, inline=False)
            embed.set_thumbnail(url=cover_image_url)
            
            if cover_image_url:
                embed.set_thumbnail(url=cover_image_url)
                dominant_color = get_dominant_color(cover_image_url)
                if dominant_color:
                    embed.color = discord.Color(int(rgb_to_hex(dominant_color).strip('#'), 16))
            else:
                embed.set_footer(text="Cover image not available.")
            
            await message.channel.send(embed=embed)
        
        elif message.content.startswith('surpass'):
            lastfm_username = 'ptrn23'
            recent_track = get_most_recent_track(lastfm_username)
            recent_track.track.username = lastfm_username
            cover_image_url = recent_track.track.get_cover_image()

            count =  recent_track.track.get_userplaycount()
            
            embed = discord.Embed(
            title=f'{recent_track.track} has now surpassed {count} scrobbles!',
            description=f"— It is the first song by the artist to surpass this milestone in {lastfm_username}'s charts!",
            color=0xff0000)
            embed.add_field(name='Milestone Date', value=recent_track.playback_date, inline=False)
            embed.set_thumbnail(url=cover_image_url)
            
            if cover_image_url:
                embed.set_thumbnail(url=cover_image_url)
                dominant_color = get_dominant_color(cover_image_url)
                if dominant_color:
                    embed.color = discord.Color(int(rgb_to_hex(dominant_color).strip('#'), 16))
            else:
                embed.set_footer(text="Cover image not available.")
            
            await message.channel.send(embed=embed)
    
    client.run(TOKEN)