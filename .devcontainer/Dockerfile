# Use Python 3.12 slim as base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    zsh \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN groupadd --gid 1000 vscode \
    && useradd --uid 1000 --gid vscode --shell /bin/zsh --create-home vscode \
    && echo "vscode ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Install uv (Python package manager)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:$PATH"

# Copy uv into the system path for all users
RUN cp /root/.cargo/bin/uv /usr/local/bin/uv

# Set the working directory
WORKDIR /workspaces/mcp-uv-base

# Copy project files
COPY pyproject.toml uv.lock ./
COPY main.py ./

# Change ownership to vscode user
RUN chown -R vscode:vscode /workspaces

# Switch to the vscode user
USER vscode

# Set up shell
RUN sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended

# Install Python dependencies using uv
RUN uv sync

# Expose the FastMCP server port
EXPOSE 3001 8000 8080

# Set the default command
CMD ["zsh"]