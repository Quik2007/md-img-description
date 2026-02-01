import fitz  # type: ignore
import os
import sys
from pathlib import Path

def extract_images_from_pdf(pdf_path: str, output_dir: str) -> list[str]:
    """
    Extracts images from a PDF file and saves them to the output directory.
    Returns a list of paths to the saved images, ordered by their appearance in the PDF.
    """
    doc = fitz.open(pdf_path)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    saved_images = []
    
    print(f"Extracting images from {pdf_path}...", file=sys.stderr)
    
    image_count = 0
    for page_index in range(len(doc)):
        page = doc[page_index]
        image_list = page.get_images()
        
        # print(f"Page {page_index + 1}: Found {len(image_list)} images", file=sys.stderr)
        
        for image_index, img in enumerate(image_list):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            
            # Handle CMYK images etc. by converting to RGB
            if pix.n - pix.alpha > 3:
                new_pix = fitz.Pixmap(fitz.csRGB, pix)
                pix = new_pix
                
            image_filename = f"image_{page_index+1}_{image_index+1}.png"
            image_filepath = output_path / image_filename
            
            pix.save(str(image_filepath))
            saved_images.append(str(image_filepath))
            image_count += 1
            
            pix = None  # Free resources
            
    print(f"Total extracted images: {len(saved_images)}", file=sys.stderr)
    return saved_images
