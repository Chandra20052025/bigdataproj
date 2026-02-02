from pyspark.sql import SparkSession
spark=SparkSession.builder\
    .appName("CompanyProfitLoss-Phase1")\
    .getOrCreate()