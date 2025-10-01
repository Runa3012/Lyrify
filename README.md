🎵 Lyrify

Lyrify is a widget-like app that tries its best to show you real-time, synced lyrics for the music you're listening to.

🚀 Features
Synced Lyrics: Real-time highlighting that follows the song.

Always-On-Top: Floats over your other windows, like games or browsers.

Romanization: Automatically converts Korean lyrics for easy sing-alongs.

Customizable: Easily change the look and feel in the static/style.css file.

🛠️ How to Run
Setup: With Python installed, open a terminal in the project folder and run:

pip install -r requirements.txt

Add Keys: Create a .env file and add your Spotify API keys. (You can get these from the Spotify Developer Dashboard).

SPOTIPY_CLIENT_ID='YOUR_CLIENT_ID'
SPOTIPY_CLIENT_SECRET='YOUR_CLIENT_SECRET'
SPOTIPY_REDIRECT_URI='[http://127.0.0.1:5000/callback](http://127.0.0.1:5000/callback)'

Remember to add http://127.0.0.1:5000/callback as a Redirect URI in your Spotify app settings.

Launch:

python app.py

Bonus: One-Click Launch (for Windows)
To open Spotify and Lyrify with a single click, you can create a simple launcher script.

In your project folder, create a new text file and rename it to launch.bat.

Right-click it, choose Edit, and paste the following code:

@echo off
echo Starting Spotify and Lyrify...

start spotify:
timeout /t 5 /nobreak >nul
start "" python app.py

exit

Now, you can just double-click launch.bat to start everything at once!

Enjoy the music!
