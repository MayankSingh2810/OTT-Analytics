-- ============================================================
-- OTT STREAM INTELLIGENCE PLATFORM
-- PERFORMANCE INDEXES
-- ============================================================

USE ott_stream_intelligence;

-- ============================================================
-- USER TABLE
-- ============================================================

CREATE INDEX idx_users_country
ON dim_users(country);

CREATE INDEX idx_users_signup
ON dim_users(signup_date);

-- ============================================================
-- CONTENT TABLE
-- ============================================================

CREATE INDEX idx_content_genre
ON dim_content(genre);

CREATE INDEX idx_content_type
ON dim_content(content_type);

CREATE INDEX idx_content_language
ON dim_content(language);

CREATE INDEX idx_content_release_year
ON dim_content(release_year);

-- ============================================================
-- WATCH HISTORY
-- ============================================================

CREATE INDEX idx_watch_user
ON fact_watch_history(user_id);

CREATE INDEX idx_watch_content
ON fact_watch_history(content_id);

CREATE INDEX idx_watch_start
ON fact_watch_history(watch_start);

CREATE INDEX idx_watch_device
ON fact_watch_history(device);

-- ============================================================
-- RATINGS
-- ============================================================

CREATE INDEX idx_rating_user
ON fact_ratings(user_id);

CREATE INDEX idx_rating_content
ON fact_ratings(content_id);

-- ============================================================
-- SEARCH
-- ============================================================

CREATE INDEX idx_search_user
ON fact_search(user_id);

CREATE INDEX idx_search_time
ON fact_search(search_time);

-- ============================================================
-- SESSIONS
-- ============================================================

CREATE INDEX idx_session_user
ON fact_sessions(user_id);

CREATE INDEX idx_session_login
ON fact_sessions(login_time);

-- ============================================================
-- SUBSCRIPTIONS
-- ============================================================

CREATE INDEX idx_subscription_user
ON fact_subscriptions(user_id);

CREATE INDEX idx_subscription_plan
ON fact_subscriptions(plan_id);

CREATE INDEX idx_subscription_status
ON fact_subscriptions(status);

-- ============================================================
-- GOLD TABLES
-- ============================================================

CREATE INDEX idx_churn
ON dim_user_features(churn_risk);

CREATE INDEX idx_favorite_genre
ON dim_user_features(favorite_genre);

CREATE INDEX idx_content_rank
ON fact_content_performance(popularity_rank);

CREATE INDEX idx_forecast_month
ON fact_forecast(forecast_month);