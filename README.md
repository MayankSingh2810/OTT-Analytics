# OTT Stream Intelligence Platform

**Enterprise Big Data Analytics & Machine Learning Platform for OTT Streaming Services**

An end-to-end enterprise-grade Big Data project that simulates a real-world OTT platform (Netflix/Prime Video/Disney+ style) using Apache Spark (PySpark), Spark Structured Streaming, MySQL, Streamlit, and Spark MLlib.

The platform continuously processes live streaming data through a Bronze → Silver → Gold Data Lake Architecture, generates business intelligence dashboards, performs churn prediction, personalized recommendations, and business forecasting.

---

## Project Highlights

- Real-Time Streaming Data Simulation
- Spark Structured Streaming
- Bronze → Silver → Gold Data Lake
- Enterprise ETL Pipeline
- Feature Store
- Random Forest Churn Prediction
- Gradient Boosted Trees
- ALS Recommendation Engine
- ARIMA Forecasting
- MySQL Data Warehouse
- Enterprise Streamlit Dashboard
- Automated Gold Pipeline Scheduler

---

## System Architecture

```
Live User Generator
        │
        ▼
Streaming Folder
        │
        ▼
Spark Structured Streaming
        │
        ▼
Bronze Layer
        │
        ▼
Silver Streaming Pipeline
        │
        ▼
Silver Batch Pipeline
        │
        ▼
Gold Layer
        │
        ├────────────► Feature Store
        │
        ├────────────► Machine Learning
        │                 │
        │                 ├── Random Forest
        │                 ├── Gradient Boosted Trees
        │                 ├── ALS Recommendation Engine
        │                 └── ARIMA Forecast
        │
        ▼
MySQL Data Warehouse
        │
        ▼
Enterprise Streamlit Dashboard
```

---

## Technology Stack

**Big Data**
- Apache Spark (PySpark)
- Spark Structured Streaming
- Parquet
- Data Lake Architecture

**Database**
- MySQL

**Machine Learning**
- Spark MLlib
- Random Forest
- Gradient Boosted Trees
- ALS Collaborative Filtering
- ARIMA Forecasting

**Dashboard**
- Streamlit
- Plotly

**Language**
- Python

---

## Data Lake Architecture

### Bronze Layer
Raw streaming datasets:
- Users
- Watch History
- Sessions
- Ratings
- Search History
- Live Events
- Content
- Subscription Plans

### Silver Layer
Cleaned & validated datasets:
- Missing value handling
- Duplicate removal
- Type conversion
- Data quality validation

### Gold Layer
Business-ready analytical datasets:
- Dashboard Summary
- Content Performance
- Genre Analytics
- Country Statistics
- Device Statistics
- User Retention
- Subscription Revenue
- Daily Active Users
- Monthly Active Users
- Watch Time Summary
- Quality Statistics

---

## Machine Learning Pipeline

### Feature Store
Production-ready engineered features for churn prediction.

**Example Features**
- Average Watch Minutes
- Completion Percentage
- Membership Years
- Days Inactive
- Device Usage
- Country

### Churn Prediction
**Algorithms**
- Random Forest
- Gradient Boosted Trees

**Evaluation Metric**
- ROC-AUC Score

### Recommendation Engine
**Algorithm**
- ALS Collaborative Filtering

**Outputs**
- Personalized Recommendations
- Predicted Ratings
- Top-N Content Recommendations

### Forecasting
**Algorithm**
- ARIMA

**Forecasts**
- Daily Active Users
- Watch Hours

---

## Dashboard Modules

**Executive Dashboard**
- Platform KPIs
- Overall Health
- Active Users
- Revenue
- Watch Time

**Content Analytics**
- Top Performing Content
- Genre Analysis
- Completion Statistics
- Watch Time Analysis

**User Analytics**
- Audience Distribution
- Membership Duration
- Country Analysis
- User Activity

**Revenue Analytics**
- Monthly Revenue
- Subscription Performance
- Auto Renew Rate
- Business KPIs

**Machine Learning Intelligence**
- Model Comparison
- Churn Analysis
- Recommendation Engine
- Forecast Dashboard
- Pipeline Health

**Real-Time Monitoring**
- Live Streaming Activity
- Infrastructure Status
- Country Traffic
- Device Distribution
- Live Event Feed

---

## ⚙️ Automation

The project supports continuous execution using live data generators and an automated scheduler.

### Live Data Generators

```bash
python generator/live_user_generator.py
```

```bash
python generator/live_event_generator.py
```

---

### Spark Structured Streaming

```bash
python -m spark_jobs.streaming_bronze_users
```

```bash
python -m spark_jobs.streaming_bronze
```

```bash
python -m spark_jobs.silver.streaming_users_pipeline
```

```bash
python -m spark_jobs.silver.streaming_pipeline
```

---

### Automatic Gold Layer Refresh

```bash
python scheduler/pipeline_scheduler.py
```

The scheduler automatically performs:

- Gold Pipeline Refresh
- MySQL Gold Loader Refresh

every **60 seconds**, keeping the dashboard synchronized with the latest streaming data.

---

## Running the Project

### Step 1 — Start Live Data Generators
```bash
python generator/live_user_generator.py
```
```bash
python generator/live_event_generator.py
```

### Step 2 — Bronze Streaming
Live Events
```bash
python -m spark_jobs.streaming_bronze
```
Live Users
```bash
python -m spark_jobs.streaming_bronze_users
```

### Step 3 — Silver Streaming
Live Events
```bash
python -m spark_jobs.silver.streaming_pipeline
```
Live Users
```bash
python -m spark_jobs.silver.streaming_users_pipeline
```

### Step 4 — Silver Batch Pipeline
```bash
python -m spark_jobs.silver.pipeline
```

### Step 5 — Gold Pipeline Scheduler

Runs automatically every 60 seconds.

```bash
python scheduler/pipeline_scheduler.py
```

The scheduler automatically:
- Builds Gold Layer
- Loads Gold tables into MySQL
- Waits 60 seconds
- Repeats

### Step 6 — Machine Learning

Run once after the Feature Store is updated.

```bash
python -m spark_jobs.ml.feature_store
```
```bash
python -m spark_jobs.ml.random_forest
```
```bash
python -m spark_jobs.ml.gradient_boosted
```
```bash
python -m spark_jobs.ml.evaluate
```
```bash
python -m spark_jobs.ml.forecast
```
```bash
python -m spark_jobs.ml.als_recommendation
```

### Step 7 — Dashboard
```bash
streamlit run dashboard/app.py
```

---

## Project Structure

```
OTT-Stream-Intelligence-Platform/

dashboard/
database/
generator/
scheduler/
└── pipeline_scheduler.py
spark_jobs/
    bronze
    silver
    gold
    ml
    live

data_lake/
    bronze/
    silver/
    gold/
    feature_store/

ml_models/
reports/
streaming/
README.md
```

---

## Enterprise Features

- Real-Time Spark Structured Streaming
- Live OTT User Simulation
- Automated ETL
- Feature Engineering
- Enterprise Machine Learning Pipeline
- Recommendation Engine
- Forecasting
- MySQL Data Warehouse
- Interactive Business Dashboard
- Automated Gold Pipeline Scheduler

---

## Skills Demonstrated

- Big Data Engineering
- Apache Spark
- Spark Structured Streaming
- ETL Development
- Data Lake Architecture
- Feature Engineering
- Machine Learning
- Recommendation Systems
- Forecasting
- Dashboard Development
- Data Warehousing
- Production Pipeline Design

---

## Future Enhancements

- Apache Kafka Integration
- Apache Airflow Orchestration
- Docker Deployment
- Kubernetes
- AWS S3 Data Lake
- Snowflake
- Cloud Deployment
- CI/CD Pipeline

---

## Author

**Mayank Singh**

Enterprise OTT Stream Intelligence Platform

Built to demonstrate practical skills in Big Data Engineering, Distributed Data Processing, Machine Learning, and Business Intelligence.