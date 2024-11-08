# Use the official Python image from Docker Hub
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install Flask

# Make port 5000 available to the world outside this container
EXPOSE 5002


# Run app.py when the container launches
CMD ["python", "app.py"]
