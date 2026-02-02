from pyspark.sql import SparkSession
from pyspark.sql.functions import sum

# Start Spark
spark = SparkSession.builder \
    .appName("CompanyProfitLoss-Phase2") \
    .getOrCreate()

# ---------------- SALES ----------------
sales_data = [
    (1, "Sales", 50000),
    (2, "Sales", 60000),
    (3, "Sales", 45000)
]

sales_df = spark.createDataFrame(
    sales_data, ["id", "department", "revenue"]
)

# ---------------- HR ----------------
hr_data = [
    (1, "HR", 20000),
    (2, "HR", 18000)
]

hr_df = spark.createDataFrame(
    hr_data, ["id", "department", "cost"]
)

# ---------------- PRODUCTION ----------------
production_data = [
    (1, "Production", 30000),
    (2, "Production", 25000)
]

production_df = spark.createDataFrame(
    production_data, ["id", "department", "cost"]
)

# ---------------- FINANCE ----------------
finance_data = [
    (1, "Finance", 10000)
]

finance_df = spark.createDataFrame(
    finance_data, ["id", "department", "cost"]
)

# ---------------- CALCULATIONS ----------------
total_revenue_df = sales_df.agg(
    sum("revenue").alias("total_revenue")
)

hr_cost_df = hr_df.agg(sum("cost").alias("hr_cost"))
prod_cost_df = production_df.agg(sum("cost").alias("prod_cost"))
fin_cost_df = finance_df.agg(sum("cost").alias("fin_cost"))

total_cost_df = hr_cost_df \
    .crossJoin(prod_cost_df) \
    .crossJoin(fin_cost_df)

final_df = total_revenue_df.crossJoin(total_cost_df) \
    .withColumn(
        "profit_or_loss",
        total_revenue_df.total_revenue -
        (total_cost_df.hr_cost +
         total_cost_df.prod_cost +
         total_cost_df.fin_cost)
    )

final_df.show()

spark.stop()
