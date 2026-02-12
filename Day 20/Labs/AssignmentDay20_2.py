import pandas as pd
import numpy as np

df = pd.read_csv("sales.csv")

df["Total"] = df["Quantity"] * df["Price"]

daily_sales = df["Total"].values

total_sales = np.sum(daily_sales)
average_sales = np.mean(daily_sales)
std_deviation = np.std(daily_sales)

print("Total Sales:", total_sales)
print("Average Daily Sales:", average_sales)
print("Standard Deviation:", std_deviation)

best_selling = df.groupby("Product")["Quantity"].sum()

print("Best Selling Product:", best_selling.idxmax())
