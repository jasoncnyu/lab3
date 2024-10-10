# Jaesung Choi
# Dockerfile for Authoritative Server (AS)
FROM python:3.8-slim

# Set working directory inside the container
WORKDIR /app

# Copy the application code
COPY . .

# Expose port 53533 for UDP connections
EXPOSE 53533/udp

# Start the Authoritative Server script
CMD ["python", "app.py"]