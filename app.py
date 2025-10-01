import os
import re
import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, jsonify
from dotenv import load_dotenv
import threading
import webview
import syncedlyrics
from langdetect import detect, DetectorFactory
import kroman
import pykakasi

load_dotenv()

DetectorFactory.seed = 0
kks = pykakasi.kakasi()
SCOPE = 'user-read-playback-state'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope=SCOPE,
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
))


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

app = Flask(__name__)
current_track_id = None
cached_lyrics = "Play a song on Spotify to see the lyrics here!"


def romanize_lyrics(lrc_text):
    try:
        sample_text = re.sub(r'\[\d{2}:\d{2}\.\d{2,3}\]', '', lrc_text)[:200]
        if not sample_text.strip():
             return lrc_text
        lang = detect(sample_text)
        if lang == 'ko' or lang == 'ja':
            new_lrc_lines = []
            for line in lrc_text.split('\n'):
                match = re.match(r'(\[\d{2}:\d{2}\.\d{2,3}\])(.*)', line)
                if match:
                    timestamp, text = match.groups()
                    romanized_text = text
                    if lang == 'ko':
                        romanized_text = kroman.parse(text)
                    elif lang == 'ja':
                        result = kks.convert(text)
                        romanized_text = ' '.join([item['romaji'] for item in result])
                    new_lrc_lines.append(timestamp + romanized_text)
                else:
                    new_lrc_lines.append(line)
            return '\n'.join(new_lrc_lines)
    except Exception as e:
        print(f"Could not process romanization. Error: {e}")
    return lrc_text

@app.route('/get_lyrics')
def get_lyrics():
    global current_track_id, cached_lyrics
    track = sp.current_playback()
    if track is not None and track['is_playing']:
        track_id = track['item']['id']
        track_name = track['item']['name']
        artist_name = track['item']['artists'][0]['name']
        progress_ms = track['progress_ms']
        if track_id != current_track_id:
            current_track_id = track_id
            lrc = syncedlyrics.search(f"{track_name} {artist_name} (Romanized)")
            if not lrc:
                lrc = syncedlyrics.search(f"{track_name} {artist_name}")
            if lrc:
                cached_lyrics = romanize_lyrics(lrc)
            else:
                cached_lyrics = "Synced lyrics not found for this track."
        return jsonify({'lyrics': cached_lyrics, 'progress_ms': progress_ms})
    return jsonify({'lyrics': "Play a song on Spotify...", 'progress_ms': 0})

@app.route('/')
def index():
    return open(resource_path('index.html')).read()


if __name__ == '__main__':
    flask_thread = threading.Thread(target=lambda: app.run(port=5000, debug=False))
    flask_thread.daemon = True
    flask_thread.start()
    try:
        sp.current_playback()
        print("Spotify connection successful.")
    except Exception as e:
        print(f"Could not connect to Spotify. Error: {e}")
        exit()
    webview.create_window(
        'Lyrify', 'http://127.0.0.1:5000/', width=400, height=400,
        frameless=True, on_top=True, easy_drag=True, transparent=True, resizable=True
    )
    webview.start()

