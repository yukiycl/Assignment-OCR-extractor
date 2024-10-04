
# Assignment OCR Extractor

This Python project uses Optical Character Recognition (OCR) to extract assignment information (such as assignment names, due dates, maximum grades, and weightings) from course images. The extracted text is saved to a structured output file, which can later be used for various purposes, including sending email reminders about upcoming assignments.

## Features

- **Image Preprocessing**: Enhances image quality before performing OCR by converting images to grayscale, applying thresholding, denoising, and resizing.
- **Text Extraction**: Utilizes `pytesseract` (Tesseract OCR) to extract text from images.
- **Text Filtering**: Filters and processes the extracted text to retain only relevant information about assignments, such as:
  - Course codes (e.g., CSC2000)
  - Assignment names (e.g., "Literature review")
  - Due dates (e.g., 22 September 2024)
  - Maximum grades (e.g., 100)
  - Weightings (e.g., 20.0%)
- **Error Handling and Logging**: Handles OCR errors gracefully and logs the extraction process for debugging.

## Planned Features

- **Email Reminders**: In future updates, the extracted assignment data will be used to send automated email reminders to students about their upcoming assignments. This will help students stay on top of deadlines and ensure they never miss a submission.

## Installation

### Prerequisites

- **Python 3.x**
- **Tesseract OCR**:
  - Install Tesseract on your system.
    - **macOS (Homebrew)**: `brew install tesseract`
    - **Ubuntu**: `sudo apt install tesseract-ocr`
    - **Windows**: Download and install from [Tesseract GitHub](https://github.com/tesseract-ocr/tesseract).
  
- **Python Libraries**:
  Install required Python packages using `pip`:
  ```bash
  pip install pytesseract Pillow opencv-python
  ```

## Usage

1. Place your assignment images in a folder (e.g., `assignment_images`).
2. Ensure that the image filenames end with common image extensions (`.png`, `.jpg`, etc.).
3. Update the `IMAGE_DIR` path in the script to point to your image folder.
4. Run the script:
   ```bash
   python ocr_script.py
   ```

5. The script will preprocess the images, extract relevant assignment information, and save it to `extracted_assignments.txt`.

### Example Output

The `extracted_assignments.txt` file will contain structured information like:

```
CSC2000
Planning a Career in the ICT Industry

Literature review 22 September 2024 100 20.0%
Reflection (personal/clinical) 27 October 2024 100 15.0%
Portfolio 03 November 2024 100 15.0%
Report 29 November 2024 100 50.0%

CSC3403
Programming 4: Advanced Paradigms

Problem Solving 8 October 2024 15 15.0%
Tech and/or scientific artefact 1 12 November 2024 20 20.0%
Tech and/or scientific artefact 2 9 December 2024 20 20.0%
Time limited online examination End of Study Period 66 45.0%

CSC3413
Network Design and Analysis

Essay 1 21 September 2024 100 10.0%
Essay 2 19 November 2024 100 20.0%
Essay 3 23 November 2024 100 20.0%
```

## Configuration

### Customizing Tesseract Path

If Tesseract OCR is not in your system's PATH, you can specify the path to the Tesseract executable in the script:
```python
pytesseract.pytesseract.tesseract_cmd = r'/path/to/tesseract'
```

### Image Preprocessing Options

The script includes several preprocessing steps to improve OCR accuracy. These include:

- **Grayscale Conversion**
- **Thresholding**
- **Denoising**
- **Resizing** (doubling the image size for better text recognition)

Feel free to modify these steps to suit the specific requirements of your images.

## Roadmap

1. **Email Reminder System**: Implement an email reminder system that will send automatic reminders about upcoming assignments, using the extracted information.


