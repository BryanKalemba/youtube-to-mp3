from flask import Flask, render_template, request, send_file
import os
import yt_dlp as youtube_dl

app = Flask(__name__)

def download_video(url, output_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.download([url])

    # Return the path to the downloaded MP3 file
    info_dict = ydl.extract_info(url, download=False)
    mp3_filename = ydl.prepare_filename(info_dict).replace('.webm', '.mp3').replace('.mp4', '.mp3')
    return mp3_filename

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    output_folder = 'downloads'
    
    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        print("Downloading and converting to MP3...")
        mp3_path = download_video(url, output_folder)
        
        print(f"MP3 file saved as: {mp3_path}")
        
        return send_file(mp3_path, as_attachment=True)
    
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True)
