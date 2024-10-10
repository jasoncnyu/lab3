# Jaesung Choi
# Dockerfile for Fibonacci Server (FS)
FROM python:3.8-slim

# Set working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 9090 for the Fibonacci server
EXPOSE 9090

# Start the Flask app
CMD ["python", "app.py"]
