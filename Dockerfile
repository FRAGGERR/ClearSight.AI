# Base image with Python
FROM python:3.12.2-slim

# Set working directory
WORKDIR /app

# Copy all files to /app in container
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose default Streamlit port
EXPOSE 8501

# Set environment variables to avoid Streamlit asking for input
ENV PYTHONUNBUFFERED=1 \
    STREAMLIT_HOME=/app \
    STREAMLIT_SECRETS=/app/.streamlit/secrets.toml

# Run the Streamlit app
CMD ["streamlit", "run", "Dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
