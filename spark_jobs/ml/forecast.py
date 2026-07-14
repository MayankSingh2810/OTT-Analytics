import os
import pandas as pd

from statsmodels.tsa.arima.model import ARIMA

# ==========================================================
# Load Gold Layer
# ==========================================================

daily = pd.read_parquet(
    "data_lake/gold/daily_active_users"
)

daily["event_date"] = pd.to_datetime(
    daily["event_date"]
)

daily = daily.sort_values(
    "event_date"
)

# ==========================================================
# Forecast Function
# ==========================================================

def create_forecast(series, days=30):

    model = ARIMA(
        series,
        order=(1,1,1)
    )

    fitted = model.fit()

    prediction = fitted.forecast(days)

    return prediction


# ==========================================================
# Forecast DAU
# ==========================================================

forecast_dau = create_forecast(
    daily["daily_active_users"]
)

# ==========================================================
# Forecast Watch Hours
# ==========================================================

forecast_watch = create_forecast(
    daily["watch_hours"]
)

# ==========================================================
# Forecast Total Events
# ==========================================================

forecast_events = create_forecast(
    daily["total_events"]
)

# ==========================================================
# Create Output
# ==========================================================

future = pd.DataFrame({

    "Day": range(1,31),

    "Forecast_DAU": forecast_dau.values,

    "Forecast_Watch_Hours": forecast_watch.values,

    "Forecast_Total_Events": forecast_events.values

})

# ==========================================================
# Save
# ==========================================================

os.makedirs(
    "ml_models/arima",
    exist_ok=True
)

future.to_parquet(

    "ml_models/arima/forecast.parquet",

    index=False

)

print("="*60)
print("ARIMA FORECAST COMPLETED")
print("="*60)

print(future.head())