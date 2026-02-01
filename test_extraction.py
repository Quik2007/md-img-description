from src.pdf_processor import extract_images_from_pdf
import os

pdf_path = "klage.pdf"
output_dir = "images"

if not os.path.exists(pdf_path):
    print(f"Error: {pdf_path} not found.")
else:
    images = extract_images_from_pdf(pdf_path, output_dir)
    print(f"Extracted {len(images)} images.")
    for img in images:
        print(f" - {img}")
