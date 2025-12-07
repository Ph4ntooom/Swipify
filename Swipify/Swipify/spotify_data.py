import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import os
from dotenv import load_dotenv
from sklearn.preprocessing import MinMaxScaler

load_dotenv()

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

sp = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    )
)

print("Client ID Loaded:", client_id)

csv_file = "Songs Dataset.csv"
df = pd.read_csv(csv_file)

print("Columns in the dataset:")
print(df.columns.tolist())

if "Unnamed: 0" in df.columns:
    df = df.drop(columns=["Unnamed: 0"])

df = df.dropna()

print("\nNull Records After Cleanup:")
print(df.isnull().sum())

df["explicit"] = df["explicit"].map({
    "TRUE": 1, "True": 1, True: 1,
    "FALSE": 0, "False": 0, False: 0
}).astype(int)

features = [
    "popularity", "duration_ms", "explicit", "danceability", "energy",
    "key", "loudness", "mode", "speechiness", "acousticness",
    "instrumentalness", "liveness", "valence", "tempo", "time_signature"
]

for col in features:
    df[col] = pd.to_numeric(df[col], errors="coerce")

scaler = MinMaxScaler()
df_scaled = scaler.fit_transform(df[features])

df_norm = df.copy()
for i, col in enumerate(features):
    df_norm[col + "_norm"] = df_scaled[:, i]

print("\nNormalized Feature Sample:")
print(df_norm[[f + "_norm" for f in features]].head())

df_norm.to_csv("Songs_Dataset_Normalized.csv", index=False)
print("\nSaved normalized dataset!")
print(df_norm.head())

