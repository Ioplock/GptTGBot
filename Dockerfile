# Use a small base image for Python 3.8
FROM python:3.8-slim

# Set working directory in the container
WORKDIR /app

# Copy requirements first for efficient caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Ensure the .env file is read inside the container
ENV PYTHONUNBUFFERED=1

# Run the bot using the module approach
CMD ["python", "-m", "bot.main"]