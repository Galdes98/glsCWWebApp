# Use an official Python runtime as a parent image
FROM python:latest

# Set the working directory to /app
WORKDIR /webapp

# Install Git
RUN apt-get update && apt-get install -y git

# Clone your Git repository
RUN git clone https://github.com/Galdes98/glsCWWebApp.git .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "manage.py", "runserver"]
