import pytest
from src.image_extractor import extract_embedded_images

def test_extract_single_image():
    content = "Here is an image: ![Test Image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==)"
    images = extract_embedded_images(content)
    assert len(images) == 1
    assert images[0].alt_text == "Test Image"
    assert images[0].mime_type == "image/png"
    assert images[0].data.startswith("iVBORw0KGgo")
    assert images[0].start_index > 0

def test_extract_multiple_images():
    content = """
    First: ![Img1](data:image/jpeg;base64,abc)
    Text
    Second: ![Img2](data:image/png;base64,def)
    """
    images = extract_embedded_images(content)
    assert len(images) == 2
    assert images[0].alt_text == "Img1"
    assert images[0].mime_type == "image/jpeg"
    assert images[1].alt_text == "Img2"
    assert images[1].mime_type == "image/png"

def test_no_images():
    content = "Just text here."
    images = extract_embedded_images(content)
    assert len(images) == 0

def test_extraction_indices():
    content = "Start ![alt](data:image/png;base64,data) End"
    images = extract_embedded_images(content)
    assert len(images) == 1
    # Check that substring extraction works
    start = images[0].start_index
    end = images[0].end_index
    assert content[start:end] == images[0].full_match
