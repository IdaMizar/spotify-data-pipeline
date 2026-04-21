import requests
import os
import base64
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")


def get_token():
    url = "https://accounts.spotify.com/api/token"

    auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
    auth_bytes = auth_str.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    headers = {
        "Authorization": f"Basic {auth_base64}"
    }

    data = {
        "grant_type": "client_credentials"
    }

    result = requests.post(url, headers=headers, data=data)
    json_result = result.json()

    return json_result["access_token"]


def get_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    result = requests.get(url, headers=headers)
    return result.json()


if __name__ == "__main__":
    token = get_token()

    artist = get_artist(token, "3TVXtAsR1Inumwj472S9r4")

    print("Artist:", artist.get("name"))

    import pandas as pd

    data = {
        "artist_name": artist.get("name"),
        "artist_id": artist.get("id"),
        "spotify_url": artist.get("external_urls", {}).get("spotify")
    }

    df = pd.DataFrame([data])

    print(df)
    df.to_csv("data/spotify_artist.csv", index=False)