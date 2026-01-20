import json
import csv
from abc import abstractmethod,ABC
from functools import wraps
import time

def log_execution(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"[LOG] Method {func.__name__}() executed successfully")
        return result
    return wrapper

def admin_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        is_admin = kwargs.get("is_admin", False)
        if not is_admin:
            raise PermissionError("Access Denied: Admin privileges required")
        return func(*args, **kwargs)
    return wrapper

def time_it(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"[TIME] {func.__name__} executed in {end - start:.4f}s")
        return result
    return wrapper

class Person(ABC):
    def __init__(self,pid,name,department):
        self.id = pid
        self.name = name
        self.department = department

    @abstractmethod
    def get_details(self):
        pass

class Student(Person):
    def __init__(self,sid, name, department, semester, marks):
        super().__init__(sid, name, department)
        self.semester = semester
        self.marks = marks

    def get_details(self):
        print("Student Details:")
        print("------------------")
        print("Name:       " + self.name)
        print("Role:       Student")
        print("Department: " + self.department)

    @log_execution
    @time_it
    def calculate_performance(self):
        avg = sum(self.marks) / len(self.marks)
        grade = "A" if avg >= 85 else "B" if avg >= 70 else "C"
        return avg, grade

    def __gt__(self, other):
        return sum(self.marks) > sum(other.marks)


class Faculty(Person):
    def __init__(self, fid, name, department, salary):
        super().__init__(fid,name,department)
        self.salary = salary

    def get_details(self):
        print("Faculty Details:")
        print("------------------")
        print("Name:       " + self.name)
        print("Role:        Faculty")
        print("Department: " + self.department)

class Course:
    def __init__(self, code, name, credits, faculty):
        self.code = code
        self.name = name
        self.credits = credits
        self.faculty = faculty

    def __add__(self, other):
        return self.credits + other.credits

    def __iter__(self):
        yield self.code
        yield self.name
        yield self.credits

class Department:
    def __init__(self, name):
        self.name = name
        self.students = []
        self.faculty = []

    def add_student(self, student):
        self.students.append(student)

    def add_faculty(self, faculty):
        self.faculty.append(faculty)

def student_generator(students):
    print("Fetching Student Records...")
    for s in students:
        yield f"{s.id} - {s.name}"

def save_students_json(students, filename="students.json"):
    data = []
    for s in students:
        data.append({
            "id": s.id,
            "name": s.name,
            "department": s.department,
            "semester": s.semester,
            "marks": s.marks
        })
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print("Student data successfully saved to students.json")


def generate_csv_report(students, filename="students_report.csv"):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Name", "Department", "Average", "Grade"])
        for s in students:
            avg, grade = s.calculate_performance()
            writer.writerow([s.id, s.name, s.department, round(avg, 2), grade])
    print("CSV Report Generated")

class MarkDescriptor:
    def __get__(self, instance, owner):
        return instance._marks

    def __set__(self, instance, value):
        for m in value:
            if m < 0 or m > 100:
                raise ValueError("Invalid Marks: Marks should be between 0 and 100")
        instance._marks = value


class SalarysDescriptor:
    def __get__(self, instance, owner):
        raise PermissionError("Access Denied: Salary is confidential")

    def __set__(self, instance, value):
        instance._salary = value

def main():
    students = []
    faculty_list = []
    courses = []

    while True:
        print("""
1. Add Student
2. Add Faculty
3. Add Course
4. Calculate Student Performance
5. Compare Two Students
6. Generate Reports
7. Exit
""")
        choice = input("Enter choice: ")

        try:
            if choice == "1":
                sid = input("Student ID: ")
                if any(s.id == sid for s in students):
                    raise ValueError("Error: Student ID already exists")

                name = input("Name: ")
                dept = input("Department: ")
                sem = int(input("Semester: "))
                marks = list(map(int, input("Marks (5 values): ").split()))

                s = Student(sid, name, dept, sem, marks)
                students.append(s)
                print("Student Created Successfully")

            elif choice == "2":
                fid = input("Faculty ID: ")
                name = input("Name: ")
                dept = input("Department: ")
                salary = int(input("Salary: "))
                f = Faculty(fid, name, dept, salary)
                faculty_list.append(f)
                print("Faculty Created Successfully")

            elif choice == "3":
                code = input("Course Code: ")
                name = input("Course Name: ")
                credits = int(input("Credits: "))
                fid = input("Faculty ID: ")
                fac = next(f for f in faculty_list if f.id == fid)
                c = Course(code, name, credits, fac)
                courses.append(c)
                print("Course Added Successfully")

            elif choice == "4":
                sid = input("Student ID: ")
                s = next(s for s in students if s.id == sid)
                avg, grade = s.calculate_performance()
                print("Average:", avg, "Grade:", grade)

            elif choice == "5":
                s1 = students[0]
                s2 = students[1]
                print(f"{s1.name} > {s2.name} :", s1 > s2)

            elif choice == "6":
                save_students_json(students)
                generate_csv_report(students)

            elif choice == "7":
                print("Thank you for using Smart University Management System")
                break

        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    main()


