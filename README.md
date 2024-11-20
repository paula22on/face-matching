# Face Matching in Newspaper Images

This project allows you to match your face against images downloaded from a newspaper website. It utilizes Python and the `face_recognition` library to detect and compare faces in a set of downloaded images with a reference image.

## Features

- Download images from a newspaper website using Python.
- Detect and compare faces in the downloaded images with a reference face.
- Supports progress logging to monitor the matching process.
- Adjustable matching tolerance for fine-tuning accuracy.

---

## Requirements

- Python 3.10 or later
- Compatible with both Apple Silicon (arm64) and Intel-based systems
- Dependencies:
  - `face_recognition`
  - `dlib`
  - `requests`
  - `beautifulsoup4`
  - `Pillow`

---

## Installation

1. **Clone the Repository**:

   ```
   git clone https://github.com/your-username/face-matching.git
   cd face-matching
   ```

2. **Set Up a Virtual Environment**:

   ```
   python3 -m venv venv
   source venv/bin/activate

   ```

3. **Install Dependencies: For macOS (Apple Silicon or Intel)**:

```
brew install cmake libjpeg
pip install -r requirements.txt
```

## Usage

### Step 1: Download Images

Run the script to scrape and download images from a specified newspaper URL:

```
python download_images.py

```

Downloaded images will be stored in the `newspaper_images/` folder.

### Step 2: Match Your Face

Add your reference image (e.g., `cara.jpg`) to the `reference_images/` folder.
Run the face-matching script:

```
python match_face.py

```

The script will compare your reference face with all downloaded images and log any matches to the terminal.

### Step 3: Monitor Progress

The script provides progress updates, such as:

```
INFO: Processing image 1/50: image_1.jpg
INFO: Match found in image_23.jpg

```

## Configuration

- Reference Image: Place your reference image in the `reference_images/` folder and update `REFERENCE_IMAGE_PATH` in `match_face.py`.
- Tolerance: Adjust the tolerance parameter in `match_face.py` to control matching sensitivity. Lower values (e.g., 0.45) are stricter.

## Code Overview

- download_images.py: Downloads images from a newspaper website using `requests` and `BeautifulSoup`.
- match_face.py: Matches a reference face against downloaded images using `face_recognition`.
- newspaper_images/: Folder for downloaded images.
- reference_images/: Folder for reference images (your face).

## License

This project is licensed under the MIT License.
