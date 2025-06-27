import os
from dotenv import load_dotenv
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, to_timestamp
from pyspark.sql.types import StructType, StringType, DoubleType

# Load environment variables from .env file
load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

S3_BUCKET = os.getenv("S3_BUCKET_NAME")

# Kafka configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BROKER")  # Change this to your Kafka broker address
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")

# S3 configuration
S3_PATH = f"s3a://{S3_BUCKET}/ETH/raw/"

CHECKPOINT_PATH = "/tmp/spark/checkpoints/eth"

# Schema for the incoming Kafka messages
schema = StructType() \
    .add("symbol", StringType()) \
    .add("price", DoubleType()) \
    .add("timestamp", StringType())

# Create a Spark session
spark = SparkSession.builder \
    .appName("StreamETHPrices") \
    .config("spark.jars.packages", ",".join([
        "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1",
        "org.apache.hadoop:hadoop-aws:3.3.4",
        "org.postgresql:postgresql:42.7.1"
    ])) \
    .getOrCreate()

# Set AWS credentials for S3 access
hadoop_conf = spark._jsc.hadoopConfiguration()
hadoop_conf.set("fs.s3a.access.key", AWS_ACCESS_KEY_ID)
hadoop_conf.set("fs.s3a.secret.key", AWS_SECRET_ACCESS_KEY)
hadoop_conf.set("fs.s3a.endpoint", "s3.amazonaws.com")

# Read from Kafka
df_kafka = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
    .option("subscribe", KAFKA_TOPIC) \
    .option("startingOffsets", "latest") \
    .load()

# Parse the JSON messages
df_parsed = df_kafka.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select(
        col("data.symbol").alias("symbol"),
        col("data.price").alias("price"),
        to_timestamp(col("data.timestamp")).alias("timestamp")
    )

# Write to S3 in Parquet format
df_parsed.writeStream \
    .format("parquet") \
    .option("checkpointLocation", CHECKPOINT_PATH) \
    .option("path", S3_PATH) \
    .outputMode("append") \
    .start()

# Write to PostgreSQL
def write_to_postgres(batch_df, _):
    batch_df.write \
        .format("jdbc") \
        .option("url", f"jdbc:postgresql://{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}") \
        .option("dbtable", "public.crypto_prices") \
        .option("user", POSTGRES_USER) \
        .option("password", POSTGRES_PASSWORD) \
        .option("driver", "org.postgresql.Driver") \
        .mode("append") \
        .save()
    
df_parsed.writeStream \
    .foreachBatch(write_to_postgres) \
    .outputMode("append") \
    .start() \
    .awaitTermination()