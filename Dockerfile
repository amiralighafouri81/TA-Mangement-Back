# Use an official Python image as the base
FROM python:3.11-bullseye
# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY ./back-end/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libmariadb-dev gcc && \
    rm -rf /var/lib/apt/lists/*


# Copy the rest of the application code
COPY ./back-end/ .

# Default command to run the server
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

