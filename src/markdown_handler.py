import re

IMAGE_PLACEHOLDER = "<!-- image -->"

def find_image_placeholders(content: str) -> list[int]:
    """
    Finds the starting indices of all image placeholders.
    """
    return [m.start() for m in re.finditer(re.escape(IMAGE_PLACEHOLDER), content)]

def get_context(content: str, index: int, window_size: int = 1000) -> str:
    """
    Extracts text context around a specific index.
    """
    start = max(0, index - window_size)
    end = min(len(content), index + len(IMAGE_PLACEHOLDER) + window_size)
    return content[start:end]

def replace_placeholder_with_description(content: str, index: int, description: str, image_path: str) -> str:
    """
    Constructs the replacement string for the placeholder.
    Note: Returns only the replacement part, not the full content handling. 
    This is a helper. The orchestration logic will handle the full string replacement carefully (to avoid index shiting issues).
    """
    # Using a blockquote for visual distinction
    replacement = f"\n> **Image Description:**\n> {description}\n>\n> ![{image_path}]({image_path})\n"
    return replacement
