import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv
import requests
from readability import Document

# Load environment variables from .env file (for local development)
load_dotenv()

app = Flask(__name__)

# --- CORS CONFIGURATION ---
# This is crucial for deployment. It allows your frontend to communicate with your backend.
# It's configured to be flexible for both local and deployed environments.
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://127.0.0.1:5500') # Default for local testing
CORS(app, resources={r"/api/*": {"origins": [FRONTEND_URL, "http://localhost:5500"]}})
# ---------------------------

# Configure the Gemini API
try:
    API_KEY = os.getenv('GEMINI_API_KEY')
    if not API_KEY:
        raise ValueError("GEMINI_API_KEY not found. Please set it in your .env file or environment variables.")
    genai.configure(api_key=API_KEY)
    # --- MODEL NAME UPDATED HERE ---
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    print(f"FATAL: Error configuring Gemini API: {e}")
    model = None

def scrape_article_content(url):
    """Scrapes the main text content and title from a given URL."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        doc = Document(response.text)
        content = doc.summary(html_partial=False)
        title = doc.title()
        return content, title
    except requests.exceptions.RequestException as e:
        print(f"Error fetching article: {e}")
        return None, None

@app.route('/api/summarize', methods=['POST'])
def summarize():
    if model is None:
        return jsonify({"error": "Server error: Gemini model is not configured correctly."}), 500
        
    data = request.get_json()
    url = data.get('url')
    length = data.get('length', 100)

    if not url:
        return jsonify({"error": "URL is required"}), 400

    article_text, article_title = scrape_article_content(url)

    if not article_text:
        return jsonify({"error": "Failed to scrape article. The website might be blocking scrapers or requires JavaScript."}), 500

    prompt = f"Summarize the following article in approximately {length} words. Provide the summary as plain text, with no special formatting, titles, or markdown.:\n\n---\n\n{article_text}"
    
    try:
        response = model.generate_content(prompt)
        return jsonify({"summary": response.text})
    except Exception as e:
        return jsonify({"error": f"Failed to generate summary from AI model: {e}"}), 500

@app.route('/api/takeaways', methods=['POST'])
def takeaways():
    if model is None:
        return jsonify({"error": "Server error: Gemini model is not configured correctly."}), 500
        
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({"error": "URL is required"}), 400

    article_text, article_title = scrape_article_content(url)

    if not article_text:
        return jsonify({"error": "Failed to scrape article."}), 500

    prompt = f"Analyze the following article and provide 3 to 5 key takeaways. Format them as a simple list using a hyphen (-) for each point. Do not add any other titles, markdown, or special formatting.:\n\n---\n\n{article_text}"
    
    try:
        response = model.generate_content(prompt)
        return jsonify({"takeaways": response.text})
    except Exception as e:
        return jsonify({"error": f"Failed to generate takeaways from AI model: {e}"}), 500

# This part is only for local development
if __name__ == '__main__':
    app.run(debug=True, port=5001)

    

