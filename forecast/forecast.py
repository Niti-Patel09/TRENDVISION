import pandas as pd
from prophet import Prophet

# Load data
df = pd.read_csv("data/reddit_posts.csv")
df['created_utc'] = pd.to_datetime(df['created_utc'], unit='s')

# Count number of posts per day
df_daily = df.groupby(df['created_utc'].dt.date).size().reset_index(name='post_count')

# Prophet requires columns: ds (date), y (value to predict)
df_daily.columns = ['ds', 'y']

# Initialize and train model
model = Prophet()
model.fit(df_daily)

# Create future dates
future = model.make_future_dataframe(periods=7)  # next 7 days

# Predict
forecast = model.predict(future)

# Save forecast
forecast[['ds', 'yhat']].to_csv("data/forecast.csv", index=False)
print("✅ Forecast saved to data/forecast.csv")
