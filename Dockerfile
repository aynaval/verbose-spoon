FROM python:3.10-alpine

# Install build dependencies and sqlite3
RUN apk add --no-cache build-base sqlite sqlite-dev

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your code
COPY . .
COPY orders.db /app/orders.db
# Expose FastAPI port
EXPOSE 8000

# Run the FastAPI app
CMD ["uvicorn", "order_tracking:app", "--host", "0.0.0.0", "--port", "8000"]
