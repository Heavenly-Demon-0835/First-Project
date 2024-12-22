import os
import pandas as pd
import requests
from googleapiclient.discovery import build
from requests.exceptions import ProxyError, HTTPError
import time
import random
import logging
from flask import Flask, request, render_template, send_file

app = Flask(__name__)

# === Configuration Section ===
# YouTube API Key (replace with your API key)
YOUTUBE_API_KEY = "YOUR_YOUTUBE_API_KEY"

# AWS Proxy server details
PROXY = {
    "http": "http://<proxy_username>:<proxy_password>@<proxy_ip>:<proxy_port>",
    "https": "http://<proxy_username>:<proxy_password>@<proxy_ip>:<proxy_port>",
}

# Initialize YouTube API
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

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

def process_excel(file_path):
    """Read an Excel file, process song names, and fetch YouTube URLs."""
    try:
        # Read the Excel file
        df = pd.read_excel(file_path)

        # Ensure 'Song Name' column exists
        if 'Song Name' not in df.columns:
            logging.error("The Excel file must contain a 'Song Name' column.")
            return

        # Add a new column for YouTube URLs
        df['YouTube URL'] = None

        for index, row in df.iterrows():
            song_name = row['Song Name']
            logging.info(f"Processing song: {song_name}")

            try:
                # Send the request through the proxy
                youtube_url = search_youtube_video(song_name)
                df.at[index, 'YouTube URL'] = youtube_url

            except ProxyError:
                logging.warning("Proxy error. Retrying...")
                time.sleep(5)
                continue

            except HTTPError as e:
                if e.response.status_code == 429:  # Too Many Requests
                    logging.warning("Rate limit hit. Retrying after delay...")
                    time.sleep(30)
                    continue
                else:
                    logging.error(f"HTTP Error: {e}")
                    df.at[index, 'YouTube URL'] = f"Error: {e}"

            time.sleep(random.uniform(2, 5))  # Random delay to avoid rate limits

        # Save the updated Excel file
        output_file = file_path.replace('.xlsx', '_with_urls.xlsx')
        df.to_excel(output_file, index=False)
        logging.info(f"Process completed. Updated file saved as {output_file}")
        return output_file

    except FileNotFoundError:
        logging.error("File not found. Please check the file path.")
    except PermissionError:
        logging.error("Permission denied. Ensure the file is not open or writable.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)
        output_file = process_excel(file_path)
        return send_file(output_file, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)