# conda activate face_env

import logging
import os

import face_recognition

# Set up logging for better monitoring
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# Path to the folder containing downloaded images
IMAGE_FOLDER = "newspaper_images"
# Path to your reference image
REFERENCE_IMAGE_PATH = "reference_images/cara_paula.jpg"


def load_and_encode_reference_image(reference_image_path):
    """Load and encode the reference face image."""
    reference_image = face_recognition.load_image_file(reference_image_path)
    reference_encoding = face_recognition.face_encodings(reference_image)
    if reference_encoding:
        logging.info("Reference face encoding created successfully.")
        return reference_encoding[0]
    else:
        logging.error("No face found in the reference image.")
        return None


def find_matching_faces(reference_encoding):
    """Search for matching faces in downloaded images."""
    matching_images = []
    total_images = len(os.listdir(IMAGE_FOLDER))  # Total number of images to process

    for idx, filename in enumerate(os.listdir(IMAGE_FOLDER), start=1):
        image_path = os.path.join(IMAGE_FOLDER, filename)
        logging.info(f"Processing image {idx}/{total_images}: {filename}")

        try:
            # Load the image and find any faces
            unknown_image = face_recognition.load_image_file(image_path)
            unknown_encodings = face_recognition.face_encodings(unknown_image)

            # Compare each face found with the reference encoding
            for unknown_encoding in unknown_encodings:
                match = face_recognition.compare_faces(
                    [reference_encoding], unknown_encoding, tolerance=0.55
                )
                if match[0]:  # If it's a match
                    matching_images.append(filename)
                    logging.info(f"Match found in {filename}")
                    break  # No need to check further faces in this image
        except Exception as e:
            logging.error(f"Failed to process {filename}: {e}")

    return matching_images


def main():
    # Step 1: Load and encode the reference image
    reference_encoding = load_and_encode_reference_image(REFERENCE_IMAGE_PATH)
    if reference_encoding is None:
        logging.error("Aborting: No reference encoding available.")
        return

    # Step 2: Find matching faces in downloaded images
    matching_images = find_matching_faces(reference_encoding)

    if matching_images:
        logging.info(f"Matching images found: {matching_images}")
    else:
        logging.info("No matches found.")


if __name__ == "__main__":
    main()
