FROM node:18-alpine

# Install system dependencies
RUN apk add --no-cache git python3 py3-pip

# Install Qodo CLI
RUN npm install -g @qodo/command

# Install MCP servers via npm
RUN npm install -g @modelcontextprotocol/server-memory @modelcontextprotocol/server-filesystem @modelcontextprotocol/server-git

# Create working directory
WORKDIR /workspace

# Copy agent configuration to working directory
COPY agent.toml /workspace/agent.toml
COPY README.md /workspace/
COPY examples/ /workspace/examples/

# Default command
CMD ["qodo", "archmind", "--help"]