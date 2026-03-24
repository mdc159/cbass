FROM python:3.13-slim

# Install uv and ffmpeg (for voice)
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg curl \
    && rm -rf /var/lib/apt/lists/* \
    && curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

# Copy project files
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY . .

# Run as non-root
RUN useradd -m donna
USER donna

CMD ["uv", "run", "python", "bot.py"]
