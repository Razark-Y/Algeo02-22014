import requests
from bs4 import BeautifulSoup
import os
import re

def sanitize_filename(filename):
    # Replace invalid filename characters with underscores
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def get_extension_from_content_type(content_type):
    if 'image/jpeg' in content_type:
        return '.jpg'
    elif 'image/png' in content_type:
        return '.png'
    elif 'image/svg+xml' in content_type:
        return '.svg'
    else:
        return ''

def download_image(url, folder, base_filename):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', '')
            print(content_type)
            extension = get_extension_from_content_type(content_type)
            if (extension == '.jpg' or extension=='.png'):
                sanitized_filename = sanitize_filename(base_filename) + extension
                full_path = os.path.join(folder, sanitized_filename)
                with open(full_path, 'wb') as f:
                    f.write(response.content)
    except Exception as e:
        print(f"Error downloading {url}: {e}")

def scrape_images(url, save_folder):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    images = soup.find_all('img')

    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    for idx, img in enumerate(images):
        src = img.get('src')
        if src: 
            image_url = src if src.startswith('http') else url + src
            base_filename = f"image_{idx}"
            download_image(image_url, save_folder, base_filename)
        src = img.get('data-src')
        if src: 
            image_url = src if src.startswith('http') else url + src
            base_filename = f"image_{idx}"
            download_image(image_url, save_folder, base_filename)