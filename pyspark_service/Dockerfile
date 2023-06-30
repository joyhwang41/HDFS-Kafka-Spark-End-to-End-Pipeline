# pyspark_service/Dockerfile

FROM python:3.9-slim-buster

# Update the sources list and Install essentials
RUN apt-get update && apt-get install -y wget openjdk-11-jdk

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Download and install Spark
ENV SPARK_VERSION=3.2.0
ENV HADOOP_VERSION=3.2
RUN wget -q https://downloads.apache.org/spark/spark-$SPARK_VERSION/spark-$SPARK_VERSION-bin-hadoop$HADOOP_VERSION.tgz && \
    tar xzf spark-$SPARK_VERSION-bin-hadoop$HADOOP_VERSION.tgz && \
    mv spark-$SPARK_VERSION-bin-hadoop$HADOOP_VERSION spark && \
    rm spark-$SPARK_VERSION-bin-hadoop$HADOOP_VERSION.tgz

# Set the SPARK_HOME environment variable
ENV SPARK_HOME=/app/spark

# Download Kafka connector for Spark
ADD https://repo1.maven.org/maven2/org/apache/spark/spark-streaming-kafka-0-10_2.12/2.4.8/spark-streaming-kafka-0-10_2.12-2.4.8.jar /spark/jars/
ADD https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/2.4.8/spark-sql-kafka-0-10_2.12-2.4.8.jar /spark/jars/

# Copy the current directory contents into the container at /app
COPY . /app

# Run app.py when the container launches
CMD ["python", "app.py"]
