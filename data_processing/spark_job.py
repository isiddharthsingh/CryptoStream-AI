from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, lit, current_timestamp, expr
from pyspark.sql.types import StructType, StructField, StringType, FloatType

# Load configurations
import json
with open('config.json') as f:
    config = json.load(f)

KAFKA_TOPIC = config['kafka_topic']
KAFKA_SERVER = config['kafka_server']
CHECKPOINT_LOCATION = config['checkpoint_location']
CSV_OUTPUT_PATH = "/Users/siddharth/Desktop/BigData_Project/coinbase_data.csv"  # Path to save CSV files (append new data)


# Initialize Spark session with Cassandra support
spark = SparkSession.builder \
    .appName("CoinbaseDataProcessing") \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.cassandra.connection.host", "localhost") \
    .config("spark.cassandra.connection.port", "9042") \
    .config("spark.cassandra.output.consistency.level", "LOCAL_QUORUM") \
    .getOrCreate()

# Define schema for incoming data
schema = StructType([
    StructField("data", StructType([
        StructField("amount", StringType()),
        StructField("base", StringType()),
        StructField("currency", StringType())
    ]))
])

# Read data from Kafka topic
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_SERVER) \
    .option("subscribe", KAFKA_TOPIC) \
    .option("failOnDataLoss", "false") \
    .option("startingOffsets", "earliest") \
    .load()

# Process and transform data
data_df = kafka_df.selectExpr("CAST(value AS STRING) as json") \
    .select(from_json(col("json"), schema).alias("parsed_data")) \
    .select(
        expr("uuid()").alias("id"),  # Generate a unique UUID for the primary key
        col("parsed_data.data.amount").cast(FloatType()).alias("amount"),
        col("parsed_data.data.base").alias("base_currency"),
        col("parsed_data.data.currency").alias("target_currency"),
        current_timestamp().alias("timestamp")  # Add a timestamp column
    )

# Print the schema to verify the structure of the DataFrame
data_df.printSchema()

# Debug the data being processed
data_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

# Write processed data to Cassandra
query = data_df.writeStream \
    .outputMode("append") \
    .format("org.apache.spark.sql.cassandra") \
    .option("keyspace", "coinbase") \
    .option("table", "processed_data") \
    .option("checkpointLocation", CHECKPOINT_LOCATION) \
    .start()

query.awaitTermination()