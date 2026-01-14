import csv
with open('student.csv',"w",newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["NAME","ID","AGE"])
    writer.writerow(["Shahrukh",10, 69])
    writer.writerow(["Salman", 11, 67])
    writer.writerow(["Aamir", 12, 66])