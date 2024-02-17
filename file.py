class FileHandler:
    """
    Class which includes methods to append to, write to and read from files
    """

    def write(self, file_name: str, data: str):
        """Method to write to a file"""
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(data)

    def read(self, file_name: str):
        """
        Method to read and write to a file
        """
        try:
            with open(file_name, "r+", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            print("\nSorry, this page is currently down for maintenance\n\n")
            exit()
        except IOError as e:
            print("An error occurred:", e)
            exit()

    def append(self, username, hashed_password, file_name: str):
        """
        Method to append to a file or create a file if it doesn't exist
        """
        with open(file_name, "a+", encoding="utf-8") as out_file:
            out_file.write("".join(f"\n{username};{hashed_password.hexdigest()}"))
            print("\n\t\tYour account has been created\n")