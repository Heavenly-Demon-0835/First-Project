import os
import pandas as pd
import tempfile
import uuid
import threading
import time
import random
import logging
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from flask import Flask, request, render_template, send_file, jsonify
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# === Configuration Section ===
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY", "YOUR_YOUTUBE_API_KEY")
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

# Background tasks storage
tasks = {}

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def search_youtube_video(song_name):
    """Search for a YouTube video using the YouTube Data API."""
    try:
        request = youtube.search().list(
            part="snippet",
            q=song_name,
            type="video",
            maxResults=1
        )
        response = request.execute()

        if response["items"]:
            video_id = response["items"][0]["id"]["videoId"]
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            return video_url
        else:
            return "No results found"

    except Exception as e:
        return f"Error: {str(e)}"

def process_excel_task(task_id, file_path):
    """Read an Excel file, process song names, fetch URLs, and track progress."""
    try:
        df = pd.read_excel(file_path)
        if 'Song Name' not in df.columns:
            tasks[task_id]['status'] = 'error'
            tasks[task_id]['error'] = "The Excel file must contain a 'Song Name' column."
            return

        df['YouTube URL'] = None
        total_rows = len(df)
        tasks[task_id]['total'] = total_rows

        for index, row in df.iterrows():
            song_name = row['Song Name']
            if pd.isna(song_name):
                continue

            try:
                youtube_url = search_youtube_video(song_name)
                df.at[index, 'YouTube URL'] = youtube_url
            except Exception as e:
                df.at[index, 'YouTube URL'] = f"Error: {e}"
            
            tasks[task_id]['current'] = index + 1
            time.sleep(random.uniform(1.0, 2.0))

        output_file = tempfile.mktemp(suffix='_with_urls.xlsx')
        df.to_excel(output_file, index=False)
        
        tasks[task_id]['status'] = 'completed'
        tasks[task_id]['result_file'] = output_file
        
    except Exception as e:
        tasks[task_id]['status'] = 'error'
        tasks[task_id]['error'] = f"An unexpected error occurred: {str(e)}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if file:
        filename = secure_filename(file.filename)
        fd, file_path = tempfile.mkstemp(suffix=filename)
        os.close(fd)
        file.save(file_path)
        
        task_id = str(uuid.uuid4())
        tasks[task_id] = {'status': 'processing', 'current': 0, 'total': 0}
        
        thread = threading.Thread(target=process_excel_task, args=(task_id, file_path))
        thread.start()
        
        return jsonify({'task_id': task_id})

@app.route('/status/<task_id>')
def get_status(task_id):
    if task_id not in tasks:
        return jsonify({'status': 'error', 'error': 'Invalid task ID'}), 404
    return jsonify(tasks[task_id])

@app.route('/download/<task_id>')
def download_file(task_id):
    if task_id not in tasks or tasks[task_id]['status'] != 'completed':
        return jsonify({'error': 'File not ready'}), 400
    return send_file(tasks[task_id]['result_file'], as_attachment=True, download_name='Processed_Songs.xlsx')

if __name__ == "__main__":
    app.run(debug=True)