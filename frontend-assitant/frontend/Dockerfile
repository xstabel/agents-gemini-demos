# Use an official Python runtime as a parent image
FROM python:3.11-slim-bookworm

# Allow statements and log messages to immediately appear in the Cloud Run logs
ENV PYTHONUNBUFFERED True

# Copy the current directory contents into the container at /app
COPY . ./

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install any needed packages specified in requirements.txt
# Install the necessary libraries
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

#Make port 8501 available
EXPOSE 8080

# Set environment variables
#ENV GOOGLE_APPLICATION_CREDENTIALS="/app/google-credentials.json"

# If you need to copy your credentials file into the container, uncomment the following line and add your credentials file:
# COPY google-credentials.json /app/
# Run cta_agent.py when the container launches
#CMD ["streamlit", "run", "cta_agent.py"]
ENTRYPOINT ["streamlit", "run", "cta_agent.py", "--server.port=8080", "--server.address=0.0.0.0"]

