import requests
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv
import os

load_dotenv()
HUGGING_FACE_API_KEY = os.getenv("HUGGING_FACE_API_KEY")

def generate_image_sd(prompt, save_file = "text_to_image/generated_image.png"):
    # URL of the Hugging Face Space hosting Stable Diffusion
    api_urls = [
        "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5",
        "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0",
    ]

    headers = {"Authorization": f"Bearer {HUGGING_FACE_API_KEY}"}
    
    payload = {
        "inputs": prompt,
    }

    response = requests.post(api_urls[0], headers=headers, json=payload)
    #response.raise_for_status()  # Ensure the request was successful
    
    # The response content is binary image data
    image = Image.open(BytesIO(response.content))
    image.save(save_file)
    return image

def main() -> None:
    while True:
        prompt = input("Enter the image prompt: ")
        generate_image_sd(prompt)
        
        print("Image saved as generated_image.png")

if __name__ == "__main__":
    main()