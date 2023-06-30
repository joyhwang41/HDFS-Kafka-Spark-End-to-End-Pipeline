# HDFS-Kafka-Spark-End-to-End-Pipeline

## Project description

This is an log analytics project, that utilized many teck-stacks, including kafka as logging service, PySpark, Spark streaming as the streaming service and distributed analysis, and finally usd HDFS as the distributed output storage system.

We will be working on a log data with size of 2.5 GB, the log entry is in the following format:
```
168.178.113.108 - - [2004-05-18 05:58:48] "GET /Archives/edgar/data/0001439124/000129281422000854/ HTTP/1.0" 500 14101
```

We will produce the data using kafka and consume it into PySpark structured streaming data. Here will be the scheme:
``` python
schema = StructType([
    StructField("host", StringType()),
    StructField("timestamp", TimestampType()),
    StructField("request", StringType()),
    StructField("http_response", IntegerType()),
    StructField("bytes_sent", IntegerType())
])
```

### File structure

``` text
├── README.md
├── Section_A_Log_Analytics_Demo.ipynb
├── data
├── docker-compose.yml
├── hdfs_service
│   ├── Dockerfile
│   └── start-hadoop.sh
├── pyspark_service
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
└── python_service
    ├── 40MBFile.log
    ├── Dockerfile
    ├── app.py
    └── requirements.txt

5 directories, 12 files


```

### Spark analysis rationale
In the Spark analysis section, we will conduct an analysis focus primary on the host, timestamp ,and the http_response fields. Aiming at specific use case as followed:

- Rate limiter service that will block a certain host if they have a reach the threshold of ceiling of request frequency, this can help prevent and lower the damage of the the service abuse, ensuring the server resource won't be exhausted by small group of people.

- Cyber security alert manager, that can detect the surge of certain kind of failed http request, since the high volume of failed http request might be a red flag of service reliabilty or potential cybersecurity issue. For example, high volume of 404 NotFound response code might be indicating a url-bustering attack from a hacker is happening.

The way we achieved this functionality is to have a moving window counter that will keep tracking on the number of request, using `count` as aggregation function and group by host name for the rate limiter service, and group by `http_response`

