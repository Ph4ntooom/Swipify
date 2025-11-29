import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import os
from dotenv import load_dotenv

#Dependencies:
#pip install flask spotipy python-dotenv scikit-learn numpy pandas

# Load .env file
load_dotenv()

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

# Connect to Spotify
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret
))

print(client_id)


csv_file = "Songs Dataset.csv"
df = pd.read_csv(csv_file)

print("Columns in the dataset:")
print(df.columns.tolist())

print("\nFirst 5 rows of the dataset:")
print(df.head())

#Make sure ur in DIR\Swipify\Swipify
#run python Swipify\\spotify_data.py

