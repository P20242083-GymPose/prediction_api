FROM python:3.12.4-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install required packages
RUN apt-get update && apt-get install -y g++ build-essential
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the outside world
EXPOSE 5000

# Define environment variable for Flask environment and default port
ENV FLASK_APP=run.py  
# Assuming your entry file is `run.py`
ENV FLASK_ENV=production  
# You might set this to `development` if debugging
ENV PORT=5000

# Run the Flask application
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]
