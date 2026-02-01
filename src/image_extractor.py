import re
from dataclasses import dataclass
from typing import List

@dataclass
class EmbeddedImage:
    full_match: str
    alt_text: str
    mime_type: str
    data: str
    start_index: int
    end_index: int

def extract_embedded_images(content: str) -> List[EmbeddedImage]:
    """
    Finds regex matches for ![alt](data:image/xyz;base64,...)
    Returns a list of EmbeddedImage objects.
    """
    # Regex pattern to match markdown image syntax with data URI
    # ![alt](data:image/type;base64,content)
    # capturing groups: 1=alt, 2=mime, 3=data
    pattern = r'!\[(.*?)\]\(data:(image/[a-zA-Z0-9]+);base64,([a-zA-Z0-9+/=]+)\)'
    
    matches = []
    for match in re.finditer(pattern, content):
        matches.append(EmbeddedImage(
            full_match=match.group(0),
            alt_text=match.group(1),
            mime_type=match.group(2),
            data=match.group(3),
            start_index=match.start(),
            end_index=match.end()
        ))
    
    return matches
