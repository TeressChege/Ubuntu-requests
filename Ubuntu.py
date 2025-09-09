import requests
import os
from urllib.parse import urlparse
import time

def create_images_directory():
    directory = "Fetched_Images"
    os.makedirs(directory, exist_ok=True)
    return directory

def extract_filename_from_url(url):
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    
    if not filename or '.' not in filename:
        timestamp = int(time.time())
        filename = f"image_{timestamp}.jpg"
    
    return filename

def fetch_image(url, directory):
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        filename = extract_filename_from_url(url)
        file_path = os.path.join(directory, filename)
        
        counter = 1
        original_name, extension = os.path.splitext(filename)
        while os.path.exists(file_path):
            filename = f"{original_name}_{counter}{extension}"
            file_path = os.path.join(directory, filename)
            counter += 1
        
        with open(file_path, 'wb') as file:
            file.write(response.content)
        
        print(f"Successfully saved: {filename}")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching image: {e}")
        return False
    except Exception as e:
        print(f"Error saving image: {e}")
        return False

def main():
    print("Ubuntu Image Fetcher")
    
    directory = create_images_directory()
    print(f"Directory created: {directory}")
    
    while True:
        url = input("Enter image URL (or 'quit' to exit): ").strip()
        
        if url.lower() in ['quit', 'exit']:
            break
        
        if not url or not url.startswith(('http://', 'https://')):
            print("Please enter a valid URL")
            continue
        
        fetch_image(url, directory)

if __name__ == "__main__":
    main()