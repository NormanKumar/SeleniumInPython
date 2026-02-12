import pandas as pd
import numpy as np

students = [
    {"name": "Alice", "score": 85},
    {"name": "Bob", "score": 92},
    {"name": "Charlie", "score": 78},
    {"name": "David", "score": 90},
    {"name": "Eva", "score": 88}
]

df = pd.DataFrame(students)

scores = df["score"].values

mean_score = np.mean(scores)
median_score = np.median(scores)
std_dev = np.std(scores)

df["above_average"] = df["score"] > mean_score

print("Mean:", mean_score)
print("Median:", median_score)
print("Standard Deviation:", std_dev)
print(df)
