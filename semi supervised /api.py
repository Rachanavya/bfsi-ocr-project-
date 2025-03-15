import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import yfinance as yf
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Define stock symbols (You can replace these with any stock symbols)
stock_symbols = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN", "META", "NVDA", "NFLX", "IBM", "ORCL"]

# Fetch stock market data
stock_data = {}
for stock in stock_symbols:
    df = yf.download(stock, period="6mo", interval="1d")  # Last 6 months
    stock_data[stock] = df["Close"].mean()  # Average Closing Price

# Convert to DataFrame
df_stocks = pd.DataFrame(list(stock_data.items()), columns=["Stock", "Avg Closing Price"])

# Normalize Data
scaler = StandardScaler()
df_stocks["Scaled Price"] = scaler.fit_transform(df_stocks[["Avg Closing Price"]])

# Apply K-Means Clustering
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)  # 3 clusters
df_stocks["Cluster"] = kmeans.fit_predict(df_stocks[["Scaled Price"]])

# Save clustered data to CSV
df_stocks.to_csv("stock_clustered_data.csv", index=False)
print("✅ Stock market clustered data saved as 'stock_clustered_data.csv'")

# Visualization: Bar Chart (Number of Stocks per Cluster)
plt.figure(figsize=(8, 5))
sns.countplot(x=df_stocks["Cluster"], palette="coolwarm")
plt.title("Number of Stocks in Each Cluster")
plt.xlabel("Cluster")
plt.ylabel("Count")
plt.show()

# Visualization: Pie Chart (Percentage of Stocks per Cluster)
plt.figure(figsize=(7, 7))
df_stocks["Cluster"].value_counts().plot.pie(autopct="%1.1f%%", cmap="coolwarm", startangle=90, shadow=True)
plt.title("Percentage of Stocks in Each Cluster")
plt.ylabel("")  # Hide y-label
plt.show()
