FROM python:3.10-slim

# Set the working directory
WORKDIR /App

# Copy the requirements file
COPY ./App/requirements.txt .

# Install the dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

RUN pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1.tar.gz


# Copy the environment variables file
COPY .env /App/.env

RUN ls -la /App/.env && cat /App/.env

# Copy the rest of the application code
COPY ./App/ .

# Expose the port that the app runs on
EXPOSE 8080

# Command to run the application
CMD ["streamlit", "run", "main.py"]