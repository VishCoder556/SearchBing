import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

def scrape_bing_images(query):
    search_url = f"https://www.bing.com/images/search?q={query}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(search_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        image_elements = soup.find_all("img")
        image_urls = []
        
        for img in image_elements:
            img_url = img.get("src")
            if img_url and img_url.startswith("http") and not img_url.startswith("https://r.bing.com"):
                # Check if the image URL is likely to be a blurred image
                if "https://tse" in img_url:  # Filtering out blurred images based on the URL pattern
                    continue  # Skip this image if it's likely blurred
                
                image_urls.append(img_url)
        
        return image_urls
    else:
        return []

@app.route('/scrape-images', methods=['GET'])
def scrape_images():
    query = request.args.get('query', '')
    image_urls = scrape_bing_images(query)
    return jsonify(image_urls)

if __name__ == '__main__':
    app.run(debug=True)
