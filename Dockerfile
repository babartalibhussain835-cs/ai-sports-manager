# Latest Python image use karein
FROM python:3.10-slim

# Working directory set karein
WORKDIR /app

# Sab se pehle system dependencies update karein
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Files copy karein
COPY . .

# Requirements install karein (No-cache use karein taake latest mal aaye)
RUN pip install --no-cache-dir -r requirements.txt

# Cloud Run ka default port 8080 hota hai
EXPOSE 8080

# Streamlit ko Cloud Run ke hisab se run karein
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
