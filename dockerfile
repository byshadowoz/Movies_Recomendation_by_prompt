FROM python:3.10-slim

# Set the working directory
WORKDIR /App

# Copy the requirements file
COPY ./App/requirements.txt .

# Install the dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

RUN pip install python-dotenv

RUN python -m spacy download en_core_web_sm

# Copy the rest of the application code
COPY ./App/ .

# Expose the port that the app runs on
EXPOSE 8080

# Command to run the application
CMD ["streamlit", "run", "main.py"]