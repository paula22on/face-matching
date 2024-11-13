import hashlib
import logging
import os

import requests
from bs4 import BeautifulSoup

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# Define constants
URLS = [
    "https://www.diariovasco.com/deportes/atletismo/behobia-sansebastian/imagenes-llegada-boulevard-sansebastian-20241110153636-ga.html",
    "https://www.diariovasco.com/deportes/atletismo/behobia-sansebastian/fotos-behobia-san-sebastian-gros-20241110124757-ga.html",
    "https://www.diariovasco.com/deportes/atletismo/behobia-sansebastian/imagenes-alto-miracruz-fotos-20241110142634-ga.html",
    "https://www.diariovasco.com/deportes/atletismo/behobia-sansebastian/fotos-behobia-san-sebastian-2024-errenteria-20241110143633-ga.html",
    "https://www.diariovasco.com/deportes/atletismo/behobia-sansebastian/corredores-behobia-paso-gaintxurizketa-20241110143052-ga.html",
    "https://www.diariovasco.com/deportes/atletismo/behobia-sansebastian/primeros-kilometros-irun-20241110152629-ga.html",
    "https://www.diariovasco.com/deportes/atletismo/behobia-sansebastian/chakib-lachgar-mireia-guarner-vencedores-behobia-san-20241110113422-ga.html",
    "https://www.diariovasco.com/deportes/atletismo/behobia-sansebastian/fotos-behobia-san-sebastian-2024-20241110144938-nt.html?ref=https%3A%2F%2Fwww.diariovasco.com%2Fdeportes%2Fatletismo%2Fbehobia-sansebastian%2Ffotos-behobia-san-sebastian-2024-20241110144938-nt.html",
    "https://www.diariovasco.com/deportes/atletismo/behobia-sansebastian/preparados-listos-20241110093531-ga.html",
]
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
}
IMAGE_FOLDER = "newspaper_images"


def fetch_html(url):
    """Fetch the HTML content of the webpage."""
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        logging.info("Page retrieved successfully.")
        return response.text
    else:
        logging.error("Failed to retrieve the webpage.")
        return None


def extract_image_urls(html_content):
    """Extract image URLs from HTML content and return unique URLs."""
    soup = BeautifulSoup(html_content, "html.parser")
    img_tags = soup.find_all("img")
    img_urls = {
        img.get("src")
        for img in img_tags
        if img.get("src") and img.get("src").startswith("http")
    }
    logging.info(f"Found {len(img_urls)} unique images.")
    return img_urls


def download_image(img_url, idx, downloaded_hashes):
    """Download an image if it’s unique and save it locally."""
    try:
        img_data = requests.get(img_url, headers=HEADERS).content
        img_hash = hashlib.md5(img_data).hexdigest()

        if img_hash not in downloaded_hashes:
            downloaded_hashes.add(img_hash)
            img_name = os.path.join(IMAGE_FOLDER, f"image_{idx+1}.jpg")
            with open(img_name, "wb") as img_file:
                img_file.write(img_data)
            logging.info(f"Downloaded {img_name}")
        else:
            logging.info(f"Skipped duplicate image from {img_url}")
    except Exception as e:
        logging.error(f"Failed to download {img_url}: {e}")


def main():
    """Main function to orchestrate downloading unique images from multiple webpages."""
    os.makedirs(IMAGE_FOLDER, exist_ok=True)

    downloaded_hashes = (
        set()
    )  # Keep track of all downloaded image hashes to avoid duplicates
    image_counter = 0  # To ensure unique file naming across all URLs

    for url in URLS:
        html_content = fetch_html(url)
        if html_content:
            img_urls = extract_image_urls(html_content)

            for img_url in img_urls:
                download_image(img_url, image_counter, downloaded_hashes)
                image_counter += 1


if __name__ == "__main__":
    main()
