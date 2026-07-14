"""
============================================================
Spark Session
============================================================
"""

from pathlib import Path

from pyspark.sql import SparkSession


BASE_DIR = Path(__file__).resolve().parent.parent

JDBC_JAR = BASE_DIR / "jars" / "mysql-connector-j-9.3.0.jar"


def create_spark_session():

    spark = (
        SparkSession.builder
        .appName("OTT Stream Intelligence Platform")
        .master("local[*]")
        .config("spark.driver.memory", "4g")
        .config("spark.executor.memory", "4g")
        .config("spark.sql.shuffle.partitions", "8")
        .config("spark.jars", str(JDBC_JAR))
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("ERROR")

    return spark