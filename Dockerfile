# Light Python image
FROM python:3.9

# Set working directory
WORKDIR /app

# COPY application files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir flask prometheus_client

# Expose Port
EXPOSE 8080

# Run the application
CMD ["python", "app.py"]
