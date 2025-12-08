from os import environ
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, render_template, request, session
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), "Swipify", ".env")
load_dotenv(dotenv_path)

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

# Initialize Spotify client
sp = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    )
)

# Load dataset
csv_file = "Songs_Dataset_Normalized.csv"
df = pd.read_csv(csv_file)

# Define audio features
features = ["danceability", "energy", "loudness", "speechiness", 
            "acousticness", "instrumentalness", "liveness", "valence", "tempo"]

def get_initial_recommendations(num=5):
    """Get random initial recommendations"""
    return df.sample(num)

def get_recommendations(user_vector, excluded_ids, num_recommendations=5):
    """Get song recommendations based on user vector"""
    # Filter out already seen songs
    df_filtered = df[~df['track_id'].isin(excluded_ids)].copy()
    
    if len(df_filtered) == 0:
        # If all songs seen, reset
        df_filtered = df.copy()
    
    song_vectors = df_filtered[features].values
    user_vector_2d = user_vector.reshape(1, -1)
    scores = cosine_similarity(user_vector_2d, song_vectors)[0]
    
    df_filtered['similarity'] = scores
    recommendations = df_filtered.sort_values(by='similarity', ascending=False).head(num_recommendations)
    
    return recommendations['track_id'].tolist()

def get_track_info(track_id):
    """Fetch track information from Spotify API"""
    try:
        track = sp.track(track_id)
        
        track_name = track["name"]
        artists = [a["name"] for a in track["artists"]]
        artist_url = track["artists"][0]["external_urls"]["spotify"]
        album_image_url = track["album"]["images"][0]["url"] if track["album"]["images"] else ""
        track_url = track["external_urls"]["spotify"]
        
        return {
            "track_id": track_id,
            "track_name": track_name,
            "artists": ", ".join(artists),
            "artist_url": artist_url,
            "album_image_url": album_image_url,
            "track_url": track_url
        }
    except Exception as e:
        print(f"Error fetching track {track_id}: {e}")
        return None

@app.route('/')
def index():
    """Initial page load with random recommendations"""
    # Initialize session variables
    session['user_vector'] = None
    session['seen_tracks'] = []
    
    # Get initial random recommendations
    initial_recs = get_initial_recommendations(5)
    track_ids = initial_recs['track_id'].tolist()
    
    tracks_info = []
    for tid in track_ids:
        info = get_track_info(tid)
        if info:
            tracks_info.append(info)
    
    return render_template('index.html', tracks=tracks_info)

@app.route('/swipe_right', methods=['POST'])
def swipe_right():
    """Handle right swipe (like)"""
    track_id = request.form.get('track_id')
    
    if not track_id:
        return "No track ID provided", 400
    
    # Get current user vector from session
    user_vector = session.get('user_vector')
    seen_tracks = session.get('seen_tracks', [])
    
    # Get song vector
    song_data = df[df['track_id'] == track_id]
    if song_data.empty:
        return "Track not found", 404
    
    song_vector = song_data[features].values[0]
    
    # Update user vector
    if user_vector is None:
        user_vector = song_vector.tolist()
    else:
        user_vector = np.array(user_vector)
        # Average with the new liked song
        user_vector = ((user_vector + song_vector) / 2).tolist()
    
    # Update session
    seen_tracks.append(track_id)
    session['user_vector'] = user_vector
    session['seen_tracks'] = seen_tracks
    
    # Get new recommendations
    track_ids = get_recommendations(np.array(user_vector), seen_tracks)
    
    tracks_info = []
    for tid in track_ids:
        info = get_track_info(tid)
        if info:
            tracks_info.append(info)
    
    return render_template('index.html', tracks=tracks_info)

@app.route('/swipe_left', methods=['POST'])
def swipe_left():
    """Handle left swipe (dislike)"""
    track_id = request.form.get('track_id')
    
    if not track_id:
        return "No track ID provided", 400
    
    # Get current user vector from session
    user_vector = session.get('user_vector')
    seen_tracks = session.get('seen_tracks', [])
    
    # Mark as seen
    seen_tracks.append(track_id)
    session['seen_tracks'] = seen_tracks
    
    # If user has preferences, penalize this song's features
    if user_vector is not None:
        song_data = df[df['track_id'] == track_id]
        if not song_data.empty:
            song_vector = song_data[features].values[0]
            user_vector = np.array(user_vector)
            # Move away from disliked song's features
            user_vector = (user_vector - 0.3 * song_vector).tolist()
            session['user_vector'] = user_vector
    
    # Get new recommendations
    if user_vector is not None:
        track_ids = get_recommendations(np.array(user_vector), seen_tracks)
    else:
        # If no preferences yet, show random songs
        initial_recs = get_initial_recommendations(5)
        track_ids = initial_recs['track_id'].tolist()
    
    tracks_info = []
    for tid in track_ids:
        info = get_track_info(tid)
        if info:
            tracks_info.append(info)
    
    return render_template('index.html', tracks=tracks_info)

@app.route('/reset')
def reset():
    """Reset user preferences"""
    session.clear()
    return index()

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '3000'))
    except ValueError:
        PORT = 3000
    app.run(HOST, PORT, debug=True)