from pyspark.sql import SparkSession

# Initialize Spark session
spark = SparkSession.builder \
    .appName("ExportCassandraToCSV") \
    .config("spark.cassandra.connection.host", "localhost") \
    .config("spark.cassandra.connection.port", "9042") \
    .getOrCreate()

# Read existing data from Cassandra
keyspace = "coinbase"
table = "processed_data"

existing_data = spark.read \
    .format("org.apache.spark.sql.cassandra") \
    .options(table=table, keyspace=keyspace) \
    .load()

# Show data for verification
existing_data.show()

# Coalesce to a single partition to write a single CSV file
csv_output_path = "/Users/siddharth/Desktop/BigData_Project/coinbase_data"

# Combine all partitions into one and write to a single CSV file
existing_data.coalesce(1) \
    .write.mode("overwrite") \
    .option("header", "true") \
    .csv(csv_output_path)

print(f"Existing data saved to {csv_output_path}")

# Stop Spark session
spark.stop()