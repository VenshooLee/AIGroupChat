FROM python:3.9-slim

WORKDIR /app

# Use Chinese mirror for faster download
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple requests

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt || \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Run application without debug mode for Docker
CMD ["python", "-u", "app.py"]
