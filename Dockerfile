FROM python:3.12

# Set the working directory in the container
WORKDIR /app

RUN mkdir -p /app/logs


# Expose 
EXPOSE 8000

# Copy Pipfile and Pipfile.lock to the working directory
COPY requirements.txt ./

# Install pipenv
#RUN pip install pipenv

# Install dependencies
#RUN pipenv lock --requirements > requirements.txt

# Install dependencies
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . ./

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]