import argparse
import sys
import os
import asyncio
from dotenv import load_dotenv
from src.processor import process_markdown
from src.server import start_server

def main():
    load_dotenv()
    
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found in environment variables.", file=sys.stderr)
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Process Markdown file to describe embedded images.")
    
    # Mutually exclusive group for modes
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument("md_path", nargs="?", help="Path to the input Markdown file")
    mode_group.add_argument("--server", action="store_true", help="Run as a REST API server")

    parser.add_argument("-o", "--output", help="Path to the output Markdown file (default: stdout)")
    parser.add_argument("--host", default="0.0.0.0", help="Host for server mode (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8000, help="Port for server mode (default: 8000)")
    
    args = parser.parse_args()
    
    if args.server:
        print(f"Starting server on {args.host}:{args.port}...", file=sys.stderr)
        start_server(args.host, args.port)
    elif args.md_path:
        md_path = args.md_path
        output_path = args.output
        
        if not os.path.exists(md_path):
            print(f"Error: Markdown file {md_path} not found.", file=sys.stderr)
            sys.exit(1)

        # Run async processor
        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        try:
            final_output = asyncio.run(process_markdown(content))
        except Exception as e:
            print(f"Error processing file: {e}", file=sys.stderr)
            sys.exit(1)
        
        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(final_output)
            print(f"Output written to {output_path}", file=sys.stderr)
        else:
            print(final_output)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
