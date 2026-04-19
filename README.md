# Excel YouTube URL Scraper

A lightweight background-processing Flask web application designed to automatically scrape and append YouTube links to a list of songs inside an Excel sheet.

## Features
- **Dynamic UI**: Beautiful modern glassmorphism frontend built with vanilla HTML/CSS/JS.
- **Background Jobs**: Eliminates HTML timeouts via threading and AJAX-based dynamic polling. 
- **Automated YouTube Discovery**: Interacts with the `google-api-python-client` to source exact URL matches.
- **Secure File Processing**: Enforces strictly handled tempfiles with zero static folder leakage.

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Heavenly-Demon-0835/First-Project.git
   cd First-Project
   ```

2. **Install Dependencies**
   Ensure you have Python 3.x installed.
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the Environment**
   Create a `.env` file in the root directory. Add your YouTube Data API Key to it:
   ```env
   YOUTUBE_API_KEY=YOUR_API_KEY_HERE
   ```

4. **Run the Server**
   ```bash
   python app.py
   ```
   Access the web interface at `http://127.0.0.1:5000`
