from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from src.processor import process_markdown
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/")
async def process_endpoint(request: Request):
    # We accept raw body as markdown
    body = await request.body()
    content = body.decode("utf-8")
    
    processed_content = await process_markdown(content)
    
    return Response(content=processed_content, media_type="text/markdown")

def start_server(host: str, port: int):
    uvicorn.run(app, host=host, port=port)
