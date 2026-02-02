from pyspark.sql import SparkSession
from pyspark.sql.functions import sum

# Start Spark Session
spark = SparkSession.builder \
    .appName("Phase3-Mixed-Format-Processing") \
    .getOrCreate()

# Read CSV files
sales_df = spark.read.csv("data/sales.csv", header=True, inferSchema=True)
hr_df = spark.read.csv("data/hr.csv", header=True, inferSchema=True)
fin_df = spark.read.csv("data/finance.csv", header=True, inferSchema=True)

# Read JSON file
prod_df = spark.read.json("data/production.json")

# Calculate totals
total_revenue = sales_df.agg(sum("amount").alias("total_revenue"))
hr_cost = hr_df.agg(sum("salary").alias("hr_cost"))
prod_cost = prod_df.agg(sum("cost").alias("prod_cost"))
fin_cost = fin_df.agg(sum("amount").alias("fin_cost"))

# Combine all results
final_df = total_revenue \
    .crossJoin(hr_cost) \
    .crossJoin(prod_cost) \
    .crossJoin(fin_cost)

# Calculate profit / loss
result_df = final_df.withColumn(
    "profit_or_loss",
    final_df.total_revenue -
    (final_df.hr_cost + final_df.prod_cost + final_df.fin_cost)
)

# Show result
result_df.show()

spark.stop()
