-- ============================================================
-- OTT STREAM INTELLIGENCE PLATFORM
-- Enterprise Data Warehouse
-- Author : Mayank Singh
-- ============================================================

DROP DATABASE IF EXISTS ott_stream_intelligence;

CREATE DATABASE ott_stream_intelligence;

USE ott_stream_intelligence;

-- ============================================================
-- DIMENSION TABLE : USERS
-- ============================================================

CREATE TABLE dim_users (

    user_id VARCHAR(20) PRIMARY KEY,

    full_name VARCHAR(120) NOT NULL,

    email VARCHAR(150) UNIQUE NOT NULL,

    gender VARCHAR(20),

    age INT,

    city VARCHAR(100),

    state VARCHAR(100),

    country VARCHAR(100),

    signup_date DATE,

    preferred_language VARCHAR(50),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

-- ============================================================
-- DIMENSION TABLE : CONTENT
-- ============================================================

CREATE TABLE dim_content (

    content_id VARCHAR(20) PRIMARY KEY,

    title VARCHAR(250) NOT NULL,

    content_type VARCHAR(30),

    genre VARCHAR(50),

    language VARCHAR(50),

    release_year INT,

    duration_minutes INT,

    age_rating VARCHAR(20),

    imdb_rating DECIMAL(3,1),

    popularity_score DECIMAL(6,2),

    production_house VARCHAR(100),

    country VARCHAR(100),

    license_cost DECIMAL(15,2),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

-- ============================================================
-- DIMENSION TABLE : SUBSCRIPTION PLAN
-- ============================================================

CREATE TABLE dim_subscription_plan (

    plan_id VARCHAR(20) PRIMARY KEY,

    plan_name VARCHAR(50),

    monthly_price DECIMAL(10,2),

    video_quality VARCHAR(30),

    screens_allowed INT,

    offline_download VARCHAR(10),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

-- ============================================================
-- DIMENSION TABLE : DATE
-- ============================================================

CREATE TABLE dim_date (

    date_key INT PRIMARY KEY,

    full_date DATE UNIQUE,

    day_of_month INT,

    month_number INT,

    month_name VARCHAR(20),

    quarter_number INT,

    year_number INT,

    week_number INT,

    day_name VARCHAR(20),

    is_weekend BOOLEAN

);

-- ============================================================
-- FACT TABLE : WATCH HISTORY
-- ============================================================

CREATE TABLE fact_watch_history (

    watch_id VARCHAR(20) PRIMARY KEY,

    user_id VARCHAR(20) NOT NULL,

    content_id VARCHAR(20) NOT NULL,

    watch_start DATETIME,

    watch_end DATETIME,

    watch_minutes DECIMAL(8,2),

    completion_pct INT,

    device VARCHAR(50),

    network VARCHAR(30),

    recommendation_source VARCHAR(50),

    liked VARCHAR(10),

    added_to_watchlist VARCHAR(10),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES dim_users(user_id),

    FOREIGN KEY (content_id)
        REFERENCES dim_content(content_id)

);
-- ============================================================
-- FACT TABLE : RATINGS
-- ============================================================

CREATE TABLE fact_ratings (

    rating_id VARCHAR(20) PRIMARY KEY,

    user_id VARCHAR(20) NOT NULL,

    content_id VARCHAR(20) NOT NULL,

    rating DECIMAL(2,1),

    review_date DATETIME,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES dim_users(user_id),

    FOREIGN KEY (content_id)
        REFERENCES dim_content(content_id)

);
-- ============================================================
-- FACT TABLE : SEARCH
-- ============================================================

CREATE TABLE fact_search (

    search_id VARCHAR(20) PRIMARY KEY,

    user_id VARCHAR(20) NOT NULL,

    search_query VARCHAR(255),

    search_time DATETIME,

    results_found INT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES dim_users(user_id)

);
-- ============================================================
-- FACT TABLE : SESSIONS
-- ============================================================

CREATE TABLE fact_sessions (

    session_id VARCHAR(20) PRIMARY KEY,

    user_id VARCHAR(20) NOT NULL,

    login_time DATETIME,

    logout_time DATETIME,

    session_minutes INT,

    device VARCHAR(50),

    operating_system VARCHAR(50),

    network VARCHAR(30),

    app_version VARCHAR(30),

    location VARCHAR(100),

    crashed VARCHAR(10),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES dim_users(user_id)

);
-- ============================================================
-- FACT TABLE : SUBSCRIPTIONS
-- ============================================================

CREATE TABLE fact_subscriptions (

    subscription_id VARCHAR(20) PRIMARY KEY,

    user_id VARCHAR(20) NOT NULL,

    plan_id VARCHAR(20) NOT NULL,

    start_date DATE,

    end_date DATE,

    status VARCHAR(30),

    auto_renew VARCHAR(10),

    payment_method VARCHAR(50),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES dim_users(user_id),

    FOREIGN KEY (plan_id)
        REFERENCES dim_subscription_plan(plan_id)

);
-- ============================================================
-- GOLD TABLE : USER FEATURES
-- ============================================================

CREATE TABLE dim_user_features (

    user_id VARCHAR(20) PRIMARY KEY,

    total_watch_minutes DECIMAL(12,2),

    avg_completion_pct DECIMAL(5,2),

    total_sessions INT,

    total_searches INT,

    total_ratings INT,

    days_since_last_watch INT,

    favorite_genre VARCHAR(50),

    preferred_device VARCHAR(50),

    binge_score INT,

    churn_risk INT,

    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES dim_users(user_id)

);
-- ============================================================
-- GOLD TABLE : CONTENT PERFORMANCE
-- ============================================================

CREATE TABLE fact_content_performance (

    content_id VARCHAR(20) PRIMARY KEY,

    total_views BIGINT,

    unique_viewers BIGINT,

    avg_watch_minutes DECIMAL(12,2),

    avg_completion_pct DECIMAL(5,2),

    avg_rating DECIMAL(3,2),

    watchlist_additions BIGINT,

    popularity_rank INT,

    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (content_id)
        REFERENCES dim_content(content_id)

);
-- ============================================================
-- GOLD TABLE : REVENUE
-- ============================================================

CREATE TABLE fact_revenue (

    revenue_date DATE PRIMARY KEY,

    active_subscribers BIGINT,

    new_subscribers BIGINT,

    churned_subscribers BIGINT,

    monthly_revenue DECIMAL(15,2),

    annual_revenue_projection DECIMAL(15,2),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);
-- ============================================================
-- GOLD TABLE : CHURN PREDICTION
-- ============================================================

CREATE TABLE fact_churn_prediction (

    user_id VARCHAR(20) PRIMARY KEY,

    churn_probability DECIMAL(5,2),

    predicted_churn VARCHAR(10),

    model_version VARCHAR(20),

    prediction_date DATETIME,

    FOREIGN KEY (user_id)
        REFERENCES dim_users(user_id)

);
-- ============================================================
-- GOLD TABLE : FORECAST
-- ============================================================

CREATE TABLE fact_forecast (

    forecast_month DATE PRIMARY KEY,

    predicted_subscribers BIGINT,

    predicted_revenue DECIMAL(15,2),

    model_name VARCHAR(50),

    confidence_score DECIMAL(5,2),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);