import os

import requests
from bs4 import BeautifulSoup

url = "https://www.diariovasco.com/deportes/atletismo/behobia-sansebastian/imagenes-llegada-boulevard-sansebastian-20241110153636-ga.html"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    html_content = response.text

    soup = BeautifulSoup(html_content, "html.parser")
    img_tags = soup.find_all("img")

    img_urls = set()
    for img in img_tags:
        img_url = img.get("src")
        # Ensure the URL is complete by checking if it starts with "http"
        if img_url and img_url.startswith("http"):
            img_urls.add(img_url)

    print(f"Found {len(img_urls)} images.")

    # Create a folder to store the images
    os.makedirs("newspaper_images", exist_ok=True)

    # Download each image
    for idx, img_url in enumerate(img_urls):
        img_data = requests.get(img_url, headers=headers).content
        img_name = f"newspaper_images/image_{idx+1}.jpg"
        with open(img_name, "wb") as img_file:
            img_file.write(img_data)
        print(f"Downloaded {img_name}")

else:
    print("Failed to retrieve the webpage.")
