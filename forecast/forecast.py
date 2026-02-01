import pandas as pd
import sys
import os
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

# Load data
if not os.path.exists("data/reddit_posts.csv"):
    print("❌ No data found. Run app.py first.")
    sys.exit(1)

df = pd.read_csv("data/reddit_posts.csv")
df['created_utc'] = pd.to_datetime(df['created_utc'], unit='s')

# Count number of posts per day
df_daily = df.groupby(df['created_utc'].dt.date).size().reset_index(name='y')
df_daily['ds'] = pd.to_datetime(df_daily['created_utc'])
df_daily = df_daily[['ds', 'y']]

if len(df_daily) < 2:
    print("⚠️ Not enough data to forecast. Creating dummy forecast.")
    # Create a dummy flat line if not enough data
    dates = pd.date_range(start=pd.Timestamp.now(), periods=7)
    forecast = pd.DataFrame({'ds': dates, 'yhat': [0]*7})
    os.makedirs("data", exist_ok=True)
    forecast.to_csv("data/forecast.csv", index=False)
    sys.exit(0)

try:
    from prophet import Prophet
    # Initialize and train model
    model = Prophet()
    model.fit(df_daily)

    # Create future dates
    future = model.make_future_dataframe(periods=7)  # next 7 days

    # Predict
    forecast = model.predict(future)
    print("✅ Forecast generated using Prophet.")

except ImportError:
    print("⚠️ Prophet not found. Using simple Moving Average fallback.")
    # Fallback: Simple Moving Average + Linear Extrapolation
    last_val = df_daily['y'].iloc[-1]
    mean_val = df_daily['y'].mean()
    
    future_dates = pd.date_range(start=df_daily['ds'].max() + pd.Timedelta(days=1), periods=7)
    # Simple logic: trend towards the mean
    future_vals = np.linspace(last_val, mean_val, 7)
    
    forecast = pd.DataFrame({'ds': future_dates, 'yhat': future_vals})
    # Append history for visualization context
    history = df_daily.rename(columns={'y': 'yhat'})
    forecast = pd.concat([history, forecast])

# Save forecast
forecast[['ds', 'yhat']].to_csv("data/forecast.csv", index=False)
print("✅ Forecast saved to data/forecast.csv")
