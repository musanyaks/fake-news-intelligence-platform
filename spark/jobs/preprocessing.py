"""Spark job for large-scale preprocessing."""
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, length, lower, regexp_replace, trim

spark = SparkSession.builder.appName("FakeNewsPreprocessing").getOrCreate()


def preprocess(input_path: str, output_path: str):
    df = spark.read.parquet(input_path)

    df = df.withColumn("clean_title", lower(trim(col("title"))))
    df = df.withColumn("clean_content", regexp_replace(col("content"), r"https?://\S+", ""))
    df = df.withColumn("text_length", length(col("content")))

    df = df.filter(col("text_length") > 100)

    df.write.mode("overwrite").parquet(output_path)
    print(f"Preprocessed data written to {output_path}")


if __name__ == "__main__":
    preprocess("s3a://fake-news-data/raw/", "s3a://fake-news-data/interim/")
