FROM python:3.12-slim-bookworm

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
# --frozen ensures we use the exact versions from uv.lock
# --no-dev excludes development dependencies (like pytest)
# --system installs into the system python environment, avoiding the need for activation
RUN uv sync --frozen --no-dev --no-install-project

# Copy output source code
COPY src/ ./src/
COPY main.py .

# Copy the project package itself if it was installed (but we are running main.py directly mostly)
# If main.py depends on the package being installed, we might need to run installs again or structure differently.
# Based on current main.py, it imports from src., so straightforward copy works if pythonpath is right.
# However, 'uv sync' typically installs the project in editable mode if not specified otherwise.
# Let's adjust PYTHONPATH to include /app.
ENV PYTHONPATH=/app

# Expose the port
EXPOSE 8000

# Command to run the server
CMD ["uv", "run", "main.py", "--server", "--host", "0.0.0.0", "--port", "8000"]
