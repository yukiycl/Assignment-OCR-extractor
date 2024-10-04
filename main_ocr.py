import pytesseract
from PIL import Image, ImageFilter
import cv2
import numpy as np
import os
import re

# path to the Tesseract exe
pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'  # Correct path

IMAGE_DIR = '/Users/nick/python/.conda'

OUTPUT_FILE = 'extracted_assignments.txt'

IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif']

# patterns to find relevant text
COURSE_CODE_PATTERN = r'CSC\d{4}'
COURSE_TITLE_PATTERN = r'^[A-Za-z0-9 :\-]+$'  
ASSIGNMENT_DETAIL_PATTERN = r'\d{1,2} [A-Za-z]+ \d{4} \d+ (\d+\.\d+%)?$'

#keyword-based matching
ASSIGNMENT_KEYWORDS = ['review', 'Reflection', 'Portfolio', 'Report',
                      'Problem Solving', 'artefact', 'Time limited', 'Exam',
                      'Essay']


def is_image_file(filename):
    return any(filename.lower().endswith(ext) for ext in IMAGE_EXTENSIONS)

def preprocess_image(image_path):
    """
    Preprocess the image to enhance OCR accuracy.
    Steps:
    1. Convert to grayscale
    2. Resize image
    3. Apply thresholding
    4. Denoise
    """
    try:
        img = cv2.imread(image_path)

        # convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # double image size
        gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)

        # gaussian blur to reduce noise
        gray = cv2.GaussianBlur(gray, (5, 5), 0)

        # thresholding
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # temp preprocessed image 
        preprocessed_image_path = 'temp_preprocessed.png'
        cv2.imwrite(preprocessed_image_path, thresh)

        return preprocessed_image_path
    except Exception as e:
        print(f"Error preprocessing {image_path}: {e}")
        return None

def extract_text_from_image(image_path):
    preprocessed_image = preprocess_image(image_path)
    if preprocessed_image is None:
        return ""
    try:
        # open image with PIL
        with Image.open(preprocessed_image) as img:
            custom_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(img, config=custom_config)
            # Remove the temp image
            os.remove(preprocessed_image)
            return text
    except Exception as e:
        print(f"Error extracting text from {image_path}: {e}")
        return ""

def filter_relevant_text(extracted_text):
    lines = extracted_text.split('\n')
    filtered_lines = []
    current_course = None
    current_course_code = None

    for line in lines:
        line = line.strip()
        if not line:
            continue  # skip empty lines

        # check for course Code
        course_code_match = re.match(COURSE_CODE_PATTERN, line)
        if course_code_match:
            current_course_code = course_code_match.group()
            current_course = current_course_code
            filtered_lines.append(current_course)
            continue

        # check for course Title
        if current_course and not any(filtered_lines[-1].startswith(prefix) for prefix in ['---', 'CSC']):
            filtered_lines.append(line)
            continue

        # check for assignment details
        assignment_detail_match = re.match(ASSIGNMENT_DETAIL_PATTERN, line)
        if assignment_detail_match:
            filtered_lines.append(line)
            continue

        # check assignment name using keywords
        if any(keyword.lower() in line.lower() for keyword in ASSIGNMENT_KEYWORDS):
            filtered_lines.append(line)
            continue

    return '\n'.join(filtered_lines)

def main():
    if not os.path.isdir(IMAGE_DIR):
        print(f"The directory '{IMAGE_DIR}' does not exist.")
        return

    image_files = [f for f in os.listdir(IMAGE_DIR) if is_image_file(f)]

    if not image_files:
        print(f"No image files found in '{IMAGE_DIR}'.")
        return

    all_extracted_text = ""

    for image_file in image_files:
        image_path = os.path.join(IMAGE_DIR, image_file)
        print(f"Processing {image_path}...")
        extracted_text = extract_text_from_image(image_path)
        relevant_text = filter_relevant_text(extracted_text)
        all_extracted_text += f"--- Text from {image_file} ---\n"
        all_extracted_text += relevant_text + "\n\n"

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(all_extracted_text)

    print(f"Extraction complete. Text saved to '{OUTPUT_FILE}'.")

if __name__ == "__main__":
    main()
