import pylast
import requests

from PIL import Image
from io import BytesIO
from colorthief import ColorThief
from key import API_KEY, API_SECRET

network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)

def get_dominant_color(image_url):
    try:
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))
        color_thief = ColorThief(BytesIO(response.content))
        dominant_color = color_thief.get_color(quality=1)
        return dominant_color
    except Exception as e:
        print(f'Error fetching dominant color: {str(e)}')
        return (255, 255, 255)

def rgb_to_hex(rgb):
    return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'