import sys
import asyncio
from src.image_extractor import extract_embedded_images
from src.ai_describer import describe_base64_image

async def process_markdown(content: str) -> str:
    """
    Processes the markdown content: finds embedded images, describes them asynchronously, 
    and returns validity markdown with descriptions replacing the images.
    """
    
    # 1. Extract Images
    images = extract_embedded_images(content)
    print(f"Found {len(images)} embedded images.", file=sys.stderr)
    
    if not images:
        return content

    # 2. Process Images in Parallel
    tasks = []
    
    for i, img in enumerate(images):
        # Get Context
        start_context = max(0, img.start_index - 1000)
        end_context = min(len(content), img.end_index + 1000)
        context_text = content[start_context:end_context]
        
        # Create Task
        tasks.append(describe_base64_image(img.data, img.mime_type, context_text))

    print(f"Describing {len(images)} images asynchronously...", file=sys.stderr)
    descriptions = await asyncio.gather(*tasks)

    # 3. Reconstruct Content
    new_content_segments = []
    last_index = 0
    
    for i, img in enumerate(images):
        # Append text before this image
        new_content_segments.append(content[last_index:img.start_index])
        
        description = descriptions[i]
        
        # Append Description ONLY (removed original image)
        segment = f"\n> **Image:**\n> {description}\n"
        new_content_segments.append(segment)
        
        last_index = img.end_index
        
    # Append remaining text
    new_content_segments.append(content[last_index:])
    
    final_output = "".join(new_content_segments)
    return final_output
