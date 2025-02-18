# Stage 1: Builder (Install Dependencies)
FROM python:3.11-slim as Builder

WORKDIR /app

# Install Dependencies
RUN apt-get update && apt-get install -y \
    wget unzip curl libnss3 libgbm1 && \
    rm -rf /var/lib/apt/lists/*

# Install Python Dependencies
COPY  requirements.txt .

# Install denpendencies to the install folder
RUN mkdir /install
RUN pip install --no-cache-dir --target=/install -r requirements.txt

# Stage 2: Final Image
FROM python:3.11-slim

WORKDIR /app

# Copy dependencies from builder stage
COPY --from=builder /install /usr/local/lib/python3.11/site-packages

# Copy Django project files
COPY . .


# Run Django server
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
