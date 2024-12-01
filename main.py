import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

def scrape_bing_images(query):
    search_url = f"https://www.bing.com/images/search?q={query}&first=1"  # Start from the first result

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    image_urls = []
    page = 1  # Track the page number
    
    while len(image_urls) < 10:  # Change to scrape only 50 images
        response = requests.get(search_url + f"&first={page * 35}")  # Pagination logic, each page has 35 results

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            image_elements = soup.find_all("img")
            
            for img in image_elements:
                img_url = img.get("src")
                if img_url and img_url.startswith("http") and not img_url.startswith("https://r.bing.com"):
                    image_urls.append(img_url)
                    
            page += 1  # Go to the next page
        else:
            break  # If we encounter an issue, stop trying
    
    # Limit to 50 images and reverse the order
    image_urls = image_urls[:10]  # Ensure only 50 images are returned
    image_urls.reverse()  # Reverse the order of the images

    return image_urls

@app.route('/scrape-images', methods=['GET'])
def scrape_images():
    query = request.args.get('query', '')
    image_urls = scrape_bing_images(query)
    return jsonify(image_urls)

if __name__ == '__main__':
    app.run(debug=True)
