# Use a Python base image
FROM python:3.9-slim

# Install dependencies
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the consumer code
COPY consumer.py consumer.py

# Run the consumer
CMD ["python", "consumer.py"]