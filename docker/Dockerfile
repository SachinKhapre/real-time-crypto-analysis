FROM bitnami/spark:3.5.1

#Set environment variables
ENV SPARK_HOME=/opt/bitnami/spark
ENV PYSPARK_PYTHON=python3

# Install required tools
USER root
RUN apt-get update && apt-get install -y \
    python3-pip python3-dev \
    curl \
    && apt-get clean

# Copy Spark jobs and .env file
COPY spark_job/ ./spark_job/
COPY .env .

# Set the working directory
WORKDIR /app

# Copy requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt