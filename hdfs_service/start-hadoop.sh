#!/bin/bash

# Check if the HDFS data directory is empty
if [ -z "$(ls -A /hadoop/dfs/data)" ]; then
   echo "HDFS data directory is empty. Formatting HDFS..."
   $HADOOP_PREFIX/bin/hdfs namenode -format
fi

# Start Hadoop services
$HADOOP_PREFIX/etc/hadoop/hadoop-env.sh
$HADOOP_PREFIX/sbin/start-dfs.sh
$HADOOP_PREFIX/sbin/start-yarn.sh

# Keep container running
tail -f /dev/null
hdfs namenode -format -force

