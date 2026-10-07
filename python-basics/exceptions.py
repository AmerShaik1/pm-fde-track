def read_file_safely(filename):
    try:
        with open(filename, "r") as file:
            return file.read()
    except FileNotFoundError:
        return f"File '{filename}' does not exist"
    except Exception as e:
        return f"Something else went wrong: {e}"

print(read_file_safely("customers.csv"))
print(read_file_safely("does_not_exist.csv"))