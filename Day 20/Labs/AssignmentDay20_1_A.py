import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="company_db"
)

cursor = conn.cursor()

cursor.execute("SELECT * FROM employees WHERE salary > 50000")
for row in cursor.fetchall():
    print(row)

cursor.execute(
    "INSERT INTO employees (name, department, salary) VALUES (%s, %s, %s)",
    ("Harsh", "IT", 60000)
)
conn.commit()

cursor.execute(
    "UPDATE employees SET salary = salary * 1.10 WHERE name = %s",
    ("Harsh",)
)
conn.commit()

cursor.close()
conn.close()
