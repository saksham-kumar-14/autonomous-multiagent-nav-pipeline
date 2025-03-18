FROM python:3.9

# Install Tkinter and Xvfb
RUN apt-get update && apt-get install -y \
    python3-tk \
    xvfb && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /autonomous-nav-pipeline

COPY requirements.txt .  
RUN pip install --no-cache-dir -r requirements.txt  

COPY . .

# Start Xvfb once and keep it running in the background
CMD Xvfb :99 -screen 0 1024x768x16 & python src/robot_controller.py

