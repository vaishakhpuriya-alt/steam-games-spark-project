# Databricks notebook source
from pyspark.sql.functions import *
from pyspark.sql.types import *

# COMMAND ----------

df = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .option("mode", "PERMISSIVE") \
    .csv("/Volumes/workspace/default/data/games.csv")

# COMMAND ----------

df.show(5)

# COMMAND ----------

from pyspark.sql.functions import *

df = df.withColumnRenamed("User score", "User_Score")

# COMMAND ----------

df.columns

# COMMAND ----------

df = df.withColumn("Platform", lit("Steam"))

# COMMAND ----------

df.show(5)

# COMMAND ----------

df = df.withColumn(
    "Game_Type",
    when(col("Price") == 0, "Free")
    .otherwise("Paid")
)

# COMMAND ----------

df.select("Name", "Price", "Game_Type").show(5)

# COMMAND ----------

paid_games = df.filter(col("Price") > 0)

paid_games.show(5)

# COMMAND ----------

df.select(
    col("Name").alias("Game_Name"),
    col("Price").alias("Game_Price"),
    col("Developers").alias("Developer")
).show(5)

# COMMAND ----------

df = df.drop("Support email")
df.columns

# COMMAND ----------

df.orderBy(col("Price").desc()).show(5)

# COMMAND ----------

df.select(
    count(when(col("Name").isNull(), 1)).alias("Name_Nulls"),
    count(when(col("Price").isNull(), 1)).alias("Price_Nulls"),
    count(when(col("Developers").isNull(), 1)).alias("Developer_Nulls"),
    count(when(col("Publishers").isNull(), 1)).alias("Publisher_Nulls")
).show()

# COMMAND ----------

df = df.fillna("Unknown")

# COMMAND ----------

df = df.fillna(0)

# COMMAND ----------

df = df.dropDuplicates()

df.count()

# COMMAND ----------

df.write.mode("overwrite").parquet("/Volumes/workspace/default/data/steam_parquet")

# COMMAND ----------

from pyspark.sql.functions import count, when, col

df.select([
    count(when(col(c).isNull(), c)).alias(c)
    for c in df.columns
]).show()

# COMMAND ----------

df = df.fillna("Unknown")

# COMMAND ----------

from pyspark.sql.functions import count, when, col

df.select([
    count(when(col(c).isNull(), c)).alias(c)
    for c in df.columns
]).show()