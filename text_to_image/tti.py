import requests
import os
from dotenv import load_dotenv
load_dotenv()

UNSPLASH_API_KEY = os.getenv("UNSPLASH_API_KEY")
BING_API_KEY = os.getenv("BING_API_KEY")

def get_image_url_bing(query, num_images=1):
    search_url = "https://api.bing.microsoft.com/v7.0/images/search"
    headers = {"Ocp-Apim-Subscription-Key": BING_API_KEY}
    params = {"q": query, "count": num_images}
    
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()

    image_urls = [img["contentUrl"] for img in search_results["value"]]

    if len(image_urls) <= 0:
        return None
    else:
        return image_urls[0]

def get_image_url_unsplash(query, num_images=1, orientation="landscape"):
    search_url = "https://api.unsplash.com/search/photos"
    headers = {"Authorization": f"Client-ID {UNSPLASH_API_KEY}"}
    params = {"query": query, "per_page": num_images, "orientation": orientation, "order_by": "relevant"}
    
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()

    image_urls = [img["urls"]["regular"] for img in search_results["results"]]

    if len(image_urls) <= 0:
        return None
    else:
        return image_urls[0]

def save_image(image_url, save_path="text_to_image/image.jpg"):
    response = requests.get(image_url)
    response.raise_for_status()
    with open(os.path.join(os.getcwd(), save_path), 'wb') as file:
        file.write(response.content)

def main() -> None:
    while True:
        query = input("Enter the image prompt: ")
        image_url = get_image_url_unsplash(query)
        
        if image_url:
            save_path = "text_to_image/image.jpg"
            save_image(image_url, save_path)
            print(f"Image saved to {save_path}")
        else:
            print("No images found.")

if __name__ == "__main__":
    main()
