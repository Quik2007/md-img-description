import base64
import os
import sys
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

# Handle DeepInfra specific base URL construction if provided
base_url = os.getenv("OPENAI_API_URL")
if base_url and "deepinfra.com" in base_url and "/v1/openai" not in base_url:
    base_url = base_url.rstrip("/") + "/v1/openai"

client = AsyncOpenAI(
    base_url=base_url,
    api_key=os.getenv("OPENAI_API_KEY"),
    max_retries=3
)

async def describe_base64_image(base64_data: str, mime_type: str, context: str) -> str:
    """
    Generates a description for a base64 encoded image using OpenAI's GPT-4o model (Async), 
    taking into account the surrounding text context.
    """
    
    prompt = f"""
    Describe this image in detail. It is part of a document. 
    Here is the surrounding text context which might help identify what the image shows:
    
    --- CONTEXT ---
    {context}
    --- END CONTEXT ---
    
    Please provide a description that can be used to understand the image content in valid Markdown format.
    Do not start with "The image shows...". Just describe it directly.
    """
    
    try:
        response = await client.chat.completions.create(
            model="Qwen/Qwen3-VL-235B-A22B-Instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{base64_data}",
                            },
                        },
                    ],
                }
            ],
            max_tokens=4092,
        )
        content = response.choices[0].message.content
        return content if content else "No description generated."
    except Exception as e:
        print(f"Error describing image: {e}", file=sys.stderr)
        return "Error generating description."

