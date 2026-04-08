FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies first for better layer caching
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app

EXPOSE 7860

# Streamlit must listen on 0.0.0.0 and HF Spaces uses port 7860
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=7860", "--server.fileWatcherType=none"]
