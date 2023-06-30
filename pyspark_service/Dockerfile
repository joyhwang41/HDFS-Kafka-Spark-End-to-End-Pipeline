FROM python:3.9-slim-buster

# Install OpenJDK
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk && \
    apt-get clean;

# Set the JAVA_HOME environment variable
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Download Kafka connector for Spark
ADD https://repo1.maven.org/maven2/org/apache/spark/spark-streaming-kafka-0-10_2.12/2.4.8/spark-streaming-kafka-0-10_2.12-2.4.8.jar /spark/jars/
ADD https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/2.4.8/spark-sql-kafka-0-10_2.12-2.4.8.jar /spark/jars/

COPY . .

CMD [ "python3", "-u", "./app.py" ]
