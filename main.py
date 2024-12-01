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
            # Check if the image URL is valid and does not contain preview patterns
            if img_url and img_url.startswith("http") and "tse" not in img_url and "th" not in img_url:
                # If there is a `data-src` attribute (full-resolution image), use it
                full_res_url = img.get("data-src", img_url)
                if full_res_url:
                    image_urls.append(full_res_url)
        
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
