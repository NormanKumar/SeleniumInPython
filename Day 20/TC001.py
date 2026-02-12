import mysql.connector
host="localhost"
user="root"
password="1234"
database="employee"

conn=mysql.connector.connect(host=host,user=user,password=password,database=database)
cursor=conn.cursor()
print("connected to the database successfully")

query="SELECT * FROM employees"
cursor.execute(query)

result=cursor.fetchall()

for row in result:
    print(row)