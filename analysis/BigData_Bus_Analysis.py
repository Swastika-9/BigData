#!/usr/bin/env python
# coding: utf-8

# # Big Data Analysis of UK Bus Timetable Data using PySpark
# 
# This notebook analyses UK Bus Open Data Service (BODS) timetable data using Apache Spark. The dataset contains over 115,000 journey pattern records extracted from XML files and converted into CSV format. The analysis demonstrates data loading, repartitioning, caching and several analytical queries using PySpark.

# # 1. Project Setup

# In[1]:


import os

os.chdir(r"C:\Users\Hp\OneDrive\Desktop\BigDataProject")

print(os.getcwd())


# In[2]:


from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("BODS Big Data Analysis")
    .master("local[*]")
    .config("spark.sql.shuffle.partitions", "4")
    .config(
        "spark.jars",
        r"C:\Users\Hp\OneDrive\Desktop\BigDataProject\mysql-connector-j-9.2.0.jar"
    )
    .getOrCreate()
)

print("Spark Version:", spark.version)


# In[3]:


journey_df = spark.read.csv(
    "data/processed/journey_pattern_links.csv",
    header=True,
    inferSchema=True
)

vehicle_df = spark.read.csv(
    "data/processed/vehicle_journeys.csv",
    header=True,
    inferSchema=True
)

operator_df = spark.read.csv(
    "data/processed/operators.csv",
    header=True,
    inferSchema=True
)


# In[10]:


from pyspark.sql.functions import regexp_extract, col

journey_df = journey_df.withColumn(
    "minutes",
    regexp_extract(col("run_time"), r"PT(\d+)M", 1).cast("int")
).withColumn(
    "seconds",
    regexp_extract(col("run_time"), r"(\d+)S", 1).cast("int")
)

journey_df = journey_df.fillna(
    0,
    subset=["minutes", "seconds"]
)

journey_df = journey_df.withColumn(
    "run_time_seconds",
    col("minutes") * 60 + col("seconds")
)


# ### Load Additional Datasets

# In[11]:


stops_df = spark.read.csv(
    "data/processed/stops.csv",
    header=True,
    inferSchema=True
)

routes_df = spark.read.csv(
    "data/processed/routes.csv",
    header=True,
    inferSchema=True
)

route_links_df = spark.read.csv(
    "data/processed/route_links.csv",
    header=True,
    inferSchema=True
)

services_df = spark.read.csv(
    "data/processed/services.csv",
    header=True,
    inferSchema=True
)

operators_df = spark.read.csv(
    "data/processed/operators.csv",
    header=True,
    inferSchema=True
)


# # 2. Data Exploration

# In[12]:


journey_df.printSchema()

print("Total Records:", journey_df.count())
print("Original Partitions:", journey_df.rdd.getNumPartitions())


# ## Repartitioning and Caching

# In[13]:


journey_df = journey_df.repartition(4)

print("Partitions:", journey_df.rdd.getNumPartitions())

journey_df.cache()

journey_df.count()

print("Dataset cached successfully.")


# ## Sample Data

# In[14]:


journey_df.show(10, truncate=False)


# ## Data Profiling

# In[15]:


from pyspark.sql.functions import mean, stddev, skewness, kurtosis

journey_df.select(
    mean("run_time_seconds").alias("Mean"),
    stddev("run_time_seconds").alias("StdDev"),
    skewness("run_time_seconds").alias("Skewness"),
    kurtosis("run_time_seconds").alias("Kurtosis")
).show()


# In[16]:


journey_df.approxQuantile(
    "run_time_seconds",
    [0.5],
    0.01
)


# In[104]:


journey_df.filter(
    journey_df.run_time_seconds > 600
).show()


# # 3 — PySpark SQL Analysis

# In[18]:


journey_df.createOrReplaceTempView("journeys")


# In[19]:


spark.sql("""
SELECT
    from_stop,
    COUNT(*) AS Total_Journeys
FROM journeys
GROUP BY from_stop
ORDER BY Total_Journeys DESC
LIMIT 10
""").show()


# # 4. Exploratory Data Analysis

# ## Analysis 1: Number of Vehicle Journeys by Operator

# In[20]:


journeys_by_operator = (
    vehicle_df.groupBy("operator_ref")
    .count()
)

journeys_by_operator = journeys_by_operator.join(
    operator_df,
    journeys_by_operator.operator_ref == operator_df.operator_id,
    "left"
)

journeys_by_operator.select(
    "operator_ref",
    "operator_short_name",
    "count"
).orderBy("count", ascending=False).show()


# ## Analysis 2: Earliest Departure Times

# In[21]:


vehicle_df.select(
    "vehicle_journey_code",
    "departure_time",
    "operator_ref"
).orderBy("departure_time").show(10, truncate=False)


# ## Analysis 3: Most Common Run Times

# In[22]:


journey_df.groupBy("run_time")\
.count()\
.orderBy("count", ascending=False)\
.show(10, truncate=False)


# ## Analysis 4: Stops with the Highest Number of Outgoing Links

# In[23]:


journey_df.groupBy("from_stop")\
.count()\
.orderBy("count", ascending=False)\
.show(10, truncate=False)


# # 5. Data Storage and Processing

# # Data Storage using MySQL

# In[24]:


import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "mysql+pymysql://root:1234@localhost/bus_data"
)

print("Connected successfully!")


# In[25]:


import pandas as pd
from pathlib import Path

# Folder containing your CSV files
csv_folder = Path("data/processed")

# Import every CSV into MySQL
for csv_file in csv_folder.glob("*.csv"):
    table_name = csv_file.stem

    print(f"Importing {table_name}...")

    df = pd.read_csv(csv_file)

    df.to_sql(
        table_name,
        con=engine,
        if_exists="replace",   
        index=False
    )

print("\nAll CSV files imported successfully!")


# In[26]:


jdbc_url = "jdbc:mysql://localhost:3306/bus_data"

properties = {
    "user": "root",
    "password": "1234",
    "driver": "com.mysql.cj.jdbc.Driver"
}

journey_mysql = spark.read.jdbc(
    url=jdbc_url,
    table="journey_pattern_links",
    properties=properties
)

journey_mysql.printSchema()

print("Rows:", journey_mysql.count())

journey_mysql.show(5, truncate=False)


# # Temporary SQL Table

# In[27]:


journey_mysql.createOrReplaceTempView("journey_links")

print("Temporary SQL view created.")


# In[28]:


spark.sql("""
SELECT
    run_time,
    COUNT(*) AS total
FROM journey_links
GROUP BY run_time
ORDER BY total DESC
LIMIT 10
""").show(truncate=False)


# In[29]:


spark.sql("""
SELECT
    from_stop,
    COUNT(*) AS journeys
FROM journey_links
GROUP BY from_stop
ORDER BY journeys DESC
LIMIT 10
""").show(truncate=False)


# In[30]:


spark.sql("""
SELECT
    COUNT(*) AS missing_activity
FROM journey_links
WHERE from_activity IS NULL
""").show()


# In[31]:


spark.sql("""
SELECT
    COUNT(DISTINCT from_stop) AS unique_stops
FROM journey_links
""").show()


# # Analysis 5: Identify the Highest-Risk Route Links

# In[32]:


print("="*60)
print("Analysis 5: Highest-Risk Route Links")
print("="*60)

route_risk = (
    journey_df.groupBy("route_link_ref")
    .count()
    .orderBy("count", ascending=False)
    .limit(10)
)

route_risk.show(truncate=False)


# In[33]:


route_risk_pd = route_risk.toPandas()

import matplotlib.pyplot as plt

plt.figure(figsize=(12,5))

plt.bar(
    route_risk_pd["route_link_ref"],
    route_risk_pd["count"]
)

plt.xticks(rotation=90)

plt.xlabel("Route Link")

plt.ylabel("Journey Count")

plt.title("Top 10 Highest-Risk Route Links")

plt.tight_layout()

plt.show()


# # 6. Longest Scheduled Run Times

# In[34]:


from pyspark.sql.functions import avg

longest_routes = (
    journey_df
    .groupBy("route_link_ref")
    .agg(avg("run_time_seconds").alias("avg_seconds"))
    .orderBy("avg_seconds", ascending=False)
    .limit(10)
)

longest_routes.show(truncate=False)


# In[35]:


longest_pd = longest_routes.toPandas()

plt.figure(figsize=(12,5))

plt.bar(
    longest_pd["route_link_ref"],
    longest_pd["avg_seconds"]
)

plt.xticks(rotation=90)

plt.xlabel("Route Link")

plt.ylabel("Average Run Time (seconds)")

plt.title("Top 10 Longest Route Links")

plt.tight_layout()

plt.show()


# # 7. Peak Service Hours

# In[36]:


from pyspark.sql.functions import hour

vehicle_hours = vehicle_df.withColumn(
    "hour",
    hour("departure_time")
)


# In[37]:


peak_hours = (
    vehicle_hours
    .groupBy("hour")
    .count()
    .orderBy("hour")
)

peak_hours.show(24)


# In[38]:


peak_hours_pd = peak_hours.toPandas()

plt.figure(figsize=(10,5))

plt.plot(
    peak_hours_pd["hour"],
    peak_hours_pd["count"],
    marker="o"
)

plt.title("Vehicle Journeys by Departure Hour")
plt.xlabel("Hour of Day")
plt.ylabel("Number of Vehicle Journeys")

plt.grid(True)

plt.xticks(range(24))

plt.tight_layout()

plt.show()


# In[39]:


top_routes = (
    journey_df.groupBy("route_link_ref")
    .count()
    .orderBy("count", ascending=False)
)

top_routes.show(10, truncate=False)


# # 6 — PySpark Optimisation

# ## Broadcast Join

# In[41]:


from pyspark.sql.functions import broadcast

broadcast_df = journey_df.join(
    broadcast(stops_df),
    journey_df.from_stop == stops_df.stop_point_ref,
    "left"
)

broadcast_df.select(
    "from_stop",
    "common_name",
    "run_time_seconds"
).show(10)


# ## Saving as Parquet

# In[42]:


journey_df.write.mode("overwrite").parquet("data/output/journey_pattern_links_parquet")


# In[43]:


parquet_df = spark.read.parquet("data/output/journey_pattern_links_parquet")

print("Rows:", parquet_df.count())
parquet_df.printSchema()


# In[44]:


import time

start = time.time()
spark.read.csv(
    "data/processed/journey_pattern_links.csv",
    header=True,
    inferSchema=True
).count()
csv_time = time.time() - start

start = time.time()
spark.read.parquet(
    "data/output/journey_pattern_links_parquet"
).count()
parquet_time = time.time() - start

print(f"CSV Read Time: {csv_time:.2f} seconds")
print(f"Parquet Read Time: {parquet_time:.2f} seconds")


# # 7: Machine Learning for Bus Run Time Prediction

# ## Feature Engineering

# In[45]:


from pyspark.sql.functions import (
    regexp_extract,
    col,
    hour,
    when,
    count
)


# In[46]:


route_complexity = (
    journey_df
    .groupBy("route_link_ref")
    .agg(count("*").alias("journey_count"))
)

route_complexity.show(10)


# In[47]:


ml_df = journey_df.join(
    route_complexity,
    on="route_link_ref",
    how="left"
)

ml_df.select(
    "route_link_ref",
    "journey_count",
    "run_time_seconds"
).show(10, truncate=False)


# In[48]:


from pyspark.sql.functions import sum

ml_df.select([
    sum(col(c).isNull().cast("int")).alias(c)
    for c in ml_df.columns
]).show()


# In[49]:


model_df = ml_df.select(
    "journey_count",
    "run_time_seconds"
)

model_df.show(10)


# # PySpark ML Pipeline

# ## Model 1 - Linear Regression

# In[52]:


from pyspark.ml.regression import LinearRegression

lr = LinearRegression(
    featuresCol="features",
    labelCol="run_time_seconds"
)

lr_model = lr.fit(train_df)


# In[53]:


lr_predictions = lr_model.transform(test_df)

lr_predictions.select(
    "journey_count",
    "run_time_seconds",
    "prediction"
).show(10, truncate=False)


# In[54]:


from pyspark.ml.evaluation import RegressionEvaluator

rmse_eval = RegressionEvaluator(
    labelCol="run_time_seconds",
    predictionCol="prediction",
    metricName="rmse"
)

mae_eval = RegressionEvaluator(
    labelCol="run_time_seconds",
    predictionCol="prediction",
    metricName="mae"
)

r2_eval = RegressionEvaluator(
    labelCol="run_time_seconds",
    predictionCol="prediction",
    metricName="r2"
)

print("RMSE:", rmse_eval.evaluate(lr_predictions))
print("MAE :", mae_eval.evaluate(lr_predictions))
print("R²  :", r2_eval.evaluate(lr_predictions))


# In[55]:


from pyspark.sql.functions import count

from_freq = (
    journey_df
    .groupBy("from_stop")
    .agg(count("*").alias("from_stop_frequency"))
)

from_freq.show(10)


# In[56]:


to_freq = (
    journey_df
    .groupBy("to_stop")
    .agg(count("*").alias("to_stop_frequency"))
)

to_freq.show(10)


# In[57]:


ml_df = (
    journey_df
    .join(route_complexity, on="route_link_ref", how="left")
    .join(from_freq, on="from_stop", how="left")
    .join(to_freq, on="to_stop", how="left")
)

ml_df.select(
    "journey_count",
    "from_stop_frequency",
    "to_stop_frequency",
    "run_time_seconds"
).show(10)


# In[58]:


from pyspark.ml.feature import VectorAssembler

assembler = VectorAssembler(
    inputCols=[
        "journey_count",
        "from_stop_frequency",
        "to_stop_frequency"
    ],
    outputCol="features"
)

final_df = assembler.transform(ml_df)

final_df.select(
    "features",
    "run_time_seconds"
).show(10, truncate=False)


# In[59]:


train_df, test_df = final_df.randomSplit(
    [0.8, 0.2],
    seed=42
)

print("Training:", train_df.count())
print("Testing :", test_df.count())


# In[60]:


from pyspark.ml.regression import LinearRegression

lr = LinearRegression(
    featuresCol="features",
    labelCol="run_time_seconds"
)

lr_model = lr.fit(train_df)

lr_predictions = lr_model.transform(test_df)

lr_predictions.select(
    "features",
    "run_time_seconds",
    "prediction"
).show(10, truncate=False)


# In[61]:


from pyspark.ml.evaluation import RegressionEvaluator

evaluator_rmse = RegressionEvaluator(
    labelCol="run_time_seconds",
    predictionCol="prediction",
    metricName="rmse"
)

evaluator_mae = RegressionEvaluator(
    labelCol="run_time_seconds",
    predictionCol="prediction",
    metricName="mae"
)

evaluator_r2 = RegressionEvaluator(
    labelCol="run_time_seconds",
    predictionCol="prediction",
    metricName="r2"
)

lr_rmse = evaluator_rmse.evaluate(lr_predictions)
lr_mae = evaluator_mae.evaluate(lr_predictions)
lr_r2 = evaluator_r2.evaluate(lr_predictions)

print("Linear Regression")
print("RMSE:", lr_rmse)
print("MAE :", lr_mae)
print("R²  :", lr_r2)


# ## Model 2 - Decision Tree Regression

# In[62]:


from pyspark.ml.regression import DecisionTreeRegressor

dt = DecisionTreeRegressor(
    featuresCol="features",
    labelCol="run_time_seconds",
    maxDepth=5
)

dt_model = dt.fit(train_df)

dt_predictions = dt_model.transform(test_df)

dt_rmse = evaluator_rmse.evaluate(dt_predictions)
dt_mae = evaluator_mae.evaluate(dt_predictions)
dt_r2 = evaluator_r2.evaluate(dt_predictions)

print("Decision Tree")
print("RMSE:", dt_rmse)
print("MAE :", dt_mae)
print("R²  :", dt_r2)


# ## Model 3 - Random Forest Regression

# In[63]:


from pyspark.ml.regression import RandomForestRegressor

rf = RandomForestRegressor(
    featuresCol="features",
    labelCol="run_time_seconds",
    numTrees=50,
    maxDepth=5,
    seed=42
)

rf_model = rf.fit(train_df)

rf_predictions = rf_model.transform(test_df)

rf_rmse = evaluator_rmse.evaluate(rf_predictions)
rf_mae = evaluator_mae.evaluate(rf_predictions)
rf_r2 = evaluator_r2.evaluate(rf_predictions)

print("Random Forest")
print("RMSE:", rf_rmse)
print("MAE :", rf_mae)
print("R²  :", rf_r2)


# ## Model Comparison

# In[64]:


import pandas as pd

comparison = pd.DataFrame({
    "Model": [
        "Linear Regression",
        "Decision Tree",
        "Random Forest"
    ],
    "RMSE": [
        lr_rmse,
        dt_rmse,
        rf_rmse
    ],
    "MAE": [
        lr_mae,
        dt_mae,
        rf_mae
    ],
    "R²": [
        lr_r2,
        dt_r2,
        rf_r2
    ]
})

comparison


# ## Prediction Visualization

# In[65]:


rf_pd = rf_predictions.select(
    "run_time_seconds",
    "prediction"
).toPandas()

plt.figure(figsize=(7,5))
plt.scatter(rf_pd["run_time_seconds"], rf_pd["prediction"], alpha=0.5)
plt.xlabel("Actual Run Time (seconds)")
plt.ylabel("Predicted Run Time (seconds)")
plt.title("Actual vs Predicted Run Time (Random Forest)")
plt.grid(True)
plt.show()


# # 8. Clean Up

# In[66]:


spark.stop()


# In[ ]:




