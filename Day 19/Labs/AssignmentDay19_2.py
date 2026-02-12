import pandas as pd

df = pd.read_excel("sales_data.xlsx")

print(df)

df["Total"] = df["Quantity"] * df["Price"]

df.to_excel("sales_summary.xlsx", index=False)

print(df)
