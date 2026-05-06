FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# Cài đặt Python và FFmpeg (rất quan trọng cho MoviePy)
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    ffmpeg \
    imagemagick \
    && rm -rf /var/lib/apt/lists/*

# Fix lỗi ImageMagick policy cho MoviePy TextClip
RUN sed -i 's/none/read,write/g' /etc/ImageMagick-6/policy.xml

WORKDIR /app
COPY requirements.txt .

# Cài đặt thư viện Python
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy toàn bộ code vào container
COPY . .

# Chạy pipeline
CMD ["python3", "main.py"]
