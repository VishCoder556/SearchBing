import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request
from flask_cors import CORS
from PIL import Image
from io import BytesIO

app = Flask(__name__)

CORS(app)

# Function to check if the image is likely blurred based on its resolution
def is_blurred_image(img_url):
    try:
        # Send a request to get the image
        img_response = requests.get(img_url, stream=True)
        
        # Check if the image was retrieved successfully
        if img_response.status_code == 200:
            img = Image.open(BytesIO(img_response.content))
            
            # Get image dimensions
            width, height = img.size
            
            # Define a threshold for minimal image resolution (example: 100x100)
            if width < 100 or height < 100:
                return True
            return False
    except Exception as e:
        # If there is any error (e.g., invalid image URL or bad response), return False
        return False

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
                # Skip blurred images based on resolution check
                if is_blurred_image(img_url):
                    continue
                
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
