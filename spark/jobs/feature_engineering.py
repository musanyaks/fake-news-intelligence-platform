"""Spark job for feature engineering."""
from pyspark.ml.feature import HashingTF, IDF, Tokenizer
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("FakeNewsFeatures").getOrCreate()


def extract_features(input_path: str, output_path: str):
    df = spark.read.parquet(input_path)

    tokenizer = Tokenizer(inputCol="clean_content", outputCol="words")
    words_df = tokenizer.transform(df)

    hashing_tf = HashingTF(inputCol="words", outputCol="raw_features", numFeatures=10000)
    featurized_df = hashing_tf.transform(words_df)

    idf = IDF(inputCol="raw_features", outputCol="features")
    idf_model = idf.fit(featurized_df)
    result_df = idf_model.transform(featurized_df)

    result_df.select("id", "features", "label").write.mode("overwrite").parquet(output_path)


if __name__ == "__main__":
    extract_features("s3a://fake-news-data/interim/", "s3a://fake-news-data/processed/")
