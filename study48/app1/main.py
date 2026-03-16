from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("PySpark WordCount Test").master("spark://localhost:7077").getOrCreate()