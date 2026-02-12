import matplotlib.pyplot as plt
import seaborn as sns

# Data
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
sales = [25000, 27000, 30000, 28000, 32000, 31000]

plt.figure(figsize=(8,5))
plt.plot(months, sales, marker='o', linestyle='-', color='blue')

plt.title("Monthly Sales Trend")
plt.xlabel("Months")
plt.ylabel("Sales Amount")
plt.grid(True)

plt.show()


# -------------------------
# Bar Plot (Seaborn)
# -------------------------
plt.figure(figsize=(8,5))
sns.barplot(x=months, y=sales, palette="viridis")

plt.title("Monthly Sales Comparison")
plt.xlabel("Months")
plt.ylabel("Sales Amount")
plt.grid(True)

plt.show()
