from ytmusicapi import YTMusic
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import json
import re
import sys

load_dotenv()

name = "Your playlist name"
desc = "Playlist description"
url = "https://open.spotify.com/playlist/1O1dNwJkLV59Ke6JEzET6m?si=9924513604e1412b"
playlist_id = re.findall(r"playlist\/([a-zA-Z0-9]*)", url)[0]

if not playlist_id:
    print("Invalid playlist url.")
    sys.exit()

ytmusic = YTMusic('headers_auth.json')
yt_playlist_id = ytmusic.create_playlist("Vicky's Chill Plalist", "Some chill beats curated by Vli")

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

playlist = sp.playlist(playlist_id)

for item in playlist["tracks"]["items"]:
    song = item["track"]
    artists = ""
    for artist in song["artists"]:
        artists += artist["name"] + " "
    name = song["name"]
    
    id = None
    search_results = ytmusic.search(artists + name)
    for result in search_results:
        if "song" in result["resultType"]:
            id = result["videoId"]
            break

    if id:
        ytmusic.add_playlist_items(yt_playlist_id, [id])
        print(f"Adding song {name} to the playlist.")
    
    else:
        print(f"Unable to find song {name}")

print("All done!")