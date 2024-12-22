# First-Project
This is my first project. This project is Excel spreadsheet URL scrapper.
Here is a detailed README for your project:

---

# YouTube URL Fetcher

## Overview

The YouTube URL Fetcher is a Python-based web application that allows users to upload an Excel spreadsheet containing a list of song names, then retrieves the corresponding YouTube URLs for each song and updates the Excel file. The application uses the YouTube Data API to search for the videos and Flask to handle the web server functionalities.

## Features

- **Upload Excel File**: Users can upload an Excel file containing a list of song names.
- **Fetch YouTube URLs**: The application searches YouTube for each song and retrieves the URL of the top result.
- **Download Updated File**: Users can download the updated Excel file with the YouTube URLs.

## Prerequisites

- Python 3.x
- YouTube Data API Key
- The following Python packages:
  - Flask
  - pandas
  - requests
  - google-api-python-client
  - openpyxl

## Installation

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/yourusername/youtube-url-fetcher.git
    cd youtube-url-fetcher
    ```

2. **Install the Required Packages**:
    ```sh
    pip install flask pandas requests google-api-python-client openpyxl
    ```

3. **Configure the Project**:
    - Replace `YOUR_YOUTUBE_API_KEY` in `app.py` with your actual YouTube API key.
    - If you are using a proxy, replace the proxy details in the `PROXY` dictionary with your actual proxy information.

## Usage

1. **Run the Application**:
    ```sh
    python app.py
    ```

2. **Access the Application**:
    - Open your web browser and go to `http://127.0.0.1:5000/`.

3. **Upload the Excel File**:
    - Use the web interface to upload an Excel file containing a list of song names.

4. **Download the Updated File**:
    - After processing, download the updated Excel file with the YouTube URLs.

## Code Explanation

### Backend (Flask)

- **app.py**: This file contains the main logic for the application.
  - **Imports**: Necessary libraries for handling data, making requests, logging, and using Flask.
  - **Configuration**: Set up API keys, proxy settings, and initialize the YouTube API.
  - **Logging**: Set up logging to track events.
  - **Functions**:
    - `search_youtube_video(song_name)`: Searches for a YouTube video using the YouTube Data API.
    - `process_excel(file_path)`: Reads the Excel file, processes song names, and fetches YouTube URLs.
  - **Routes**:
    - `/`: Renders the homepage.
    - `/upload`: Handles file upload, processes the file, and returns the updated file.
  - **Run Flask**: Starts the Flask server.

### Frontend (HTML + Bootstrap)

- **index.html**: The HTML file for the frontend, located in the `templates` folder.
  - **HTML Structure**: Basic structure of an HTML document.
  - **Bootstrap**: A CSS framework for building responsive and modern web pages.
  - **Form**:
    - `action="/upload"`: Specifies the URL where the form data will be sent.
    - `method="post"`: Indicates that the form should be submitted using the POST method.
    - `enctype="multipart/form-data"`: Allows file uploads.
  - **JavaScript**: Includes necessary scripts for Bootstrap functionality.

## Issues and Considerations

- **No Backend API**: The project does not contain a dedicated backend API for handling requests. Instead, it uses Flask to manage web server functionalities and directly process the uploaded files.
- **Rate Limits**: The YouTube Data API has rate limits. If the rate limit is exceeded, the application will wait for a period before retrying.
- **Proxy Settings**: If you are using a proxy, ensure that the proxy settings are correctly configured in the `PROXY` dictionary.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes. 
