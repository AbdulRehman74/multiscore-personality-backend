# Use an official Python runtime as a parent image
FROM python:3.10

# Set environment variable so that Poetry doesn’t create its own virtual environment
ENV POETRY_VIRTUALENVS_CREATE=false

# Optionally, you can set a specific Poetry version
ENV POETRY_VERSION=2.0.1

# Set the working directory in the container
WORKDIR /app

# Install Poetry using pip
RUN pip install "poetry==$POETRY_VERSION"

# Copy the pyproject.toml file to leverage Docker layer caching
COPY pyproject.toml /app/

# Install project dependencies using Poetry
RUN poetry install --no-interaction --no-ansi --no-root

# Now copy the rest of the project files into the container
COPY . /app

# Expose port 8000 for the FastAPI app
EXPOSE 8000

# Set additional environment variables as needed
ENV QUESTIONS_FILE=app/static/questions.json

# Run the FastAPI application using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]