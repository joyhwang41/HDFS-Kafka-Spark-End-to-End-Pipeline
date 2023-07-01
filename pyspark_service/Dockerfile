FROM python:3.9-slim-buster

# Install OpenJDK and wget
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk wget && \
    apt-get clean;

# Set the JAVA_HOME environment variable
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

WORKDIR /app

# Download the Spark Kafka integration jars
RUN mkdir -p jars && \
    wget -P jars/ https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.2.0/spark-sql-kafka-0-10_2.12-3.2.0.jar && \
    wget -P jars/ https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/2.8.0/kafka-clients-2.8.0.jar && \
    wget -P jars/ https://repo1.maven.org/maven2/org/spark-project/spark/unused/1.0.0/unused-1.0.0.jar

# Add these jars to PySpark classpath
ENV PYSPARK_SUBMIT_ARGS="--jars /app/jars/spark-sql-kafka-0-10_2.12-3.2.0.jar,/app/jars/kafka-clients-2.8.0.jar,/app/jars/unused-1.0.0.jar pyspark-shell"

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-u", "./app.py" ]
