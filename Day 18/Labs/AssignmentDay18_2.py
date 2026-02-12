import pandas as pd

data = {
    "Employee": ["John", "Alice", "Bob", "Eva", "Mark"],
    "Department": ["IT", "HR", "IT", "Finance", "HR"],
    "Salary": [50000, 60000, 55000, 65000, 62000]
}

df = pd.DataFrame(data)

it_employees = df[df["Department"] == "IT"]

avg_salary_per_dept = df.groupby("Department")["Salary"].mean()

df["Salary_Adjusted"] = df["Salary"] * 1.10

print("IT Employees:")
print(it_employees)

print("\nAverage Salary per Department:")
print(avg_salary_per_dept)

print("\nUpdated DataFrame:")
print(df)
