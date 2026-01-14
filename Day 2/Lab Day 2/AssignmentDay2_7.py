from AssignmentDay2_6 import write_numbers_to_file

def read_file(filename):
    try:
        with open(filename, "r") as file:
            content = file.read()
            print("File Content:\n")
            print(content)

    except FileNotFoundError:
        print("Error: File not found.")

    except PermissionError:
        print("Error: Permission denied.")

    except Exception as e:
        print("Unexpected error:", e)


if __name__ == "__main__":
    filename = "numbers.txt"
    write_numbers_to_file(filename)
    read_file(filename)
