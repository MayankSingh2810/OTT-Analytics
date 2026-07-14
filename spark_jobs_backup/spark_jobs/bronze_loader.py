"""
============================================================
Bronze Loader
============================================================
"""

from config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
    BRONZE_DIR,
)

from spark_jobs.spark_session import create_spark_session


TABLES = [

    "subscription_plans",

    "users",

    "content",

    "subscriptions",

    "user_behavior",

    "watch_history",

    "ratings",

    "search_history",

    "sessions"

]


spark = create_spark_session()

jdbc_url = (
    f"jdbc:mysql://{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

properties = {

    "user": DB_USER,

    "password": DB_PASSWORD,

    "driver": "com.mysql.cj.jdbc.Driver"

}


for table in TABLES:

    print("=" * 70)

    print(f"Loading {table}")

    df = spark.read.jdbc(

        url=jdbc_url,

        table=table,

        properties=properties

    )

    print(f"Rows : {df.count():,}")

    output = BRONZE_DIR / table

    df.write.mode("overwrite").parquet(str(output))

    print(f"Saved -> {output}")

spark.stop()

print("=" * 70)

print("Bronze Layer Created Successfully")