# Summarize

This program summarizes contents of text files, websites, and image files.

In order to summarize image files, the program makes use of OpenCV to isolate text and Tesseract OCR to identify characters.

### Running summarize

To run summarize, enter `python summarize.py` followed by the following:
- `--text your_text.txt` for text files
- `--url https://yourlinkhere.com` for web sites
- `--image your_img.jpg` for images

Other input types are currently under development.
