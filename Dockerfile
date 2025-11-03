# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the API code and its requirements
COPY api/ /app/api/

# Install the dependencies
RUN pip install --no-cache-dir -r /app/api/requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run the API server
# This command is run when the container launches
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]


