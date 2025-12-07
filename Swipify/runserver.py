from os import environ
from Swipify import app
import pandas as pd
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

dotenv_path = os.path.join(os.path.dirname(__file__), "Swipify", ".env")
load_dotenv(dotenv_path)

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

sp = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    )
)

csv_file = "Songs_Dataset_Normalized.csv"
df = pd.read_csv(csv_file)

initial_recommendation = df.sample(5)


def get_track_info(track_id):
    track = sp.track(track_id)

    # Track name
    track_name = track["name"]

    # Artist(s) name(s) and first artist URL
    artists = [a["name"] for a in track["artists"]]
    artist_url = track["artists"][0]["external_urls"]["spotify"]

    # Album image (biggest)
    album_image_url = track["album"]["images"][0]["url"]

    # Track Spotify URL
    track_url = track["external_urls"]["spotify"]

    return {
        "track_id": track_id,
        "track_name": track_name,
        "artists": ", ".join(artists),
        "artist_url": artist_url,
        "album_image_url": album_image_url,
        "track_url": track_url
    }

tracks_info = [get_track_info(tid) for tid in initial_recommendation["track_id"]]
print(tracks_info)

user_vector

# Gotta Embed The SONG    
#<iframe src="https://open.spotify.com/embed/track/{{ track_id }}" width="300" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>


#if __name__ == '__main__':
#    HOST = environ.get('SERVER_HOST', 'localhost')
#   try:
#       PORT = int(environ.get('SERVER_PORT', '5555'))
#    except ValueError:
#        PORT = 5555
#    app.run(HOST, PORT)

