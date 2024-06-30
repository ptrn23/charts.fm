import random
import pylast
from key import API_KEY, API_SECRET

network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)

def handle_response(message) -> str:
    p_message = message.lower()
    print(p_message)
    
    if p_message == "hello":
        return "hey"
    
    if p_message == "roll":
        return str(random.randint(1,6))
    
    if p_message == "!help":
        return "`Help!`"
    
    if p_message == "recent":
        lastfm_username = 'ptrn23'
        recent_track = get_most_recent_track(lastfm_username)
        if recent_track:
            return f'Most recent track for {lastfm_username}: {recent_track.track}'
            
def get_most_recent_track(username: str):
    try:
        last_user = network.get_user(username)
        recent_track = last_user.get_recent_tracks(limit=1)[0]
        print(recent_track)
        
        return recent_track
    except Exception as e:
        print(f'Error fetching recent track: {str(e)}')
        return None
    