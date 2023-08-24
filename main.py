import os
from flask import Flask, render_template, request, session, flash
import subprocess
import yt_dlp as ydl

app = Flask(__name__)
app.secret_key = 'golan04'

def download_music_from_url(url):
    try:
        subprocess.run(['yt-dlp', '-x', '--audio-format', 'mp3', '--audio-quality', '320K', '-o', '~/Downloads/%(title)s.%(ext)s', url], check=True)
        return "Download completed successfully!"
    except subprocess.CalledProcessError as e:
        return f"An error occurred during download: {e}"

def download_music_by_search(song_name):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'outtmpl': '~/Desktop/%(title)s.%(ext)s'
    }

    try:
        with ydl.YoutubeDL(ydl_opts) as ydl_instance:
            info_dict = ydl_instance.extract_info(f"ytsearch1:{song_name}", download=True)
            if 'entries' in info_dict:
                downloaded_file_title = info_dict['entries'][0]['title']
                query_cleared = False
                if query_cleared:
                    song_name = ""

                return f"Downloaded '{downloaded_file_title}.mp3' successfully!"
            else:
                return "No results found."
    except Exception as e:
        return f"An error occurred during download: {e}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_data = request.form['input_data']

        if "://" in input_data:
            url = input_data
            song_name = ""
        else:
            url = ""
            song_name = input_data

        if url:
            result = download_music_from_url(url)
        elif song_name:
            result = download_music_by_search(song_name)

        
        session['download_completed'] = True
        flash(result)  
    else:
        result = None
    
    session.pop('download_completed', None)
    flash(None)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000)
