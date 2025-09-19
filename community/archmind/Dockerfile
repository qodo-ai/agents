FROM node:18-alpine

# Install system dependencies
RUN apk add --no-cache git python3 py3-pip

# Install Qodo CLI
RUN npm install -g @qodo/cli

# Install MCP servers
RUN pip3 install mcp-server-filesystem mcp-server-git mcp-server-memory

# Create working directory
WORKDIR /workspace

# Copy agent configuration
COPY agent.toml /workspace/
COPY README.md /workspace/
COPY examples/ /workspace/examples/

# Set up environment
ENV NODE_ENV=production
ENV MCP_SERVERS_PATH=/workspace

# Default command
CMD ["qodo", "archmind", "--help"]
