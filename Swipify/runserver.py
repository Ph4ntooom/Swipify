from os import environ
from sklearn.metrics.pairwise import cosine_similarity
from Flask import flask, render_template, request
from Swipify import app
import pandas as pd
import numpy as np
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

features = ["danceability", "energy", "loudness", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo"]


def get_recommendations(user_vector, last_track_id, num_recommendations=5):
    df_filtered = df[df['track_id'] != last_track_id].copy()

    song_vectors = df_filtered[features].values
    user_vector_2d = user_vector.reshape(1, -1)

    scores = cosine_similarity(user_vector_2d, song_vectors)[0]
    
    df_filtered['similarity'] = scores
    recommendations = df_filtered.sort_values(by='similarity', ascending=False).head(num_recommendations)

    recommended_tracks_info = [get_track_info(tid) for tid in recommendations['track_id']]
    return recommended_tracks_info

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



# print(tracks_info)


# Gotta Embed The SONG    
#<iframe src="https://open.spotify.com/embed/track/{{ track_id }}" width="300" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>

user_vector = None

@app.route('/swipe_right', methods=['GET', 'POST'])
def swipe_right():
    global user_vector
    if request.method == 'POST':
        track_id = request.form['track_id']
        song_vector = df[df['track_id'] == track_id][features].values[0]

        if user_vector is None:
            user_vector = song_vector
        else:
            user_vector = ((user_vector + song_vector) / 2)

        recommendations = get_recommendations(user_vector, track_id)
        return render_template('index.html', tracks=recommendations)
    return render_template('index.html', tracks=tracks_info)

@app.route('/swipe_left', methods=['GET', 'POST'])
def swipe_left():
    if request.method == 'POST':
        track_id = request.form['track_id']
        recommendations = get_recommendations(user_vector, track_id)
        return render_template('index.html', tracks=recommendations)
    return render_template('index.html', tracks=tracks_info)


if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '3000'))
    except ValueError:
         PORT = 3000
    app.run(HOST, PORT)