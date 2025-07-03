#!/bin/bash

# Fail on first error
set -e

# Set script to run
SCRIPT_PATH=${1:-/opt/workspace/spark_job/stream_eth_prices.py}

# Submit Spark job
/opt/bitnami/spark/bin/spark-submit \
  --master local[*] \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,\
org.apache.hadoop:hadoop-aws:3.3.4,\
org.postgresql:postgresql:42.7.1 \
  "$SCRIPT_PATH"
