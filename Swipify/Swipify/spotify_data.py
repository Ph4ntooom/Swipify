import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

#Dependencies:
#pip install flask spotipy scikit-learn numpy pandas

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
    client_id="Client ID",
    client_secret="Client Secret"
))

csv_file = "Songs Dataset.csv"
df = pd.read_csv(csv_file)

print("Columns in the dataset:")
print(df.columns.tolist())

print("\nFirst 5 rows of the dataset:")
print(df.head())

#Make sure ur in DIR\Swipify\Swipify
#run python Swipify\\spotify_data.py

