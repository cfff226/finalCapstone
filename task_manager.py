# =====importing libraries===========
import os
from datetime import datetime, date
from hashlib import sha256
import sys
import subprocess
from file import FileHandler

# The pseudocode for this project is located in the task_manager.txt file
# The credentials to run this program as an admin are as follows:
# username: admin
# password: password


file = FileHandler()

DATETIME_STRING_FORMAT = "%Y-%m-%d"

curr_date = date.today()

# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w", encoding="utf-8") as default_file:
        default_file.write(
            "admin;5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
        )

# Convert to a dictionary
username_password = {}


# Clear the console
def clear():
    subprocess.run("clear", shell=True)


clear()
print("\n\t\tWelcome to the task manager\n")

# Logic enabling user to login
logged_in = False
while not logged_in:
    # Read in user data
    user_data = file.read("user.txt").split("\n")
    for user in user_data:
        user = user.split(";")
        username_password[user[0]] = user[1]

    # Request username from the user
    login_username = input("\nPlease enter your username:\n").lower()
    USERNAME_ENTERED = True
    if login_username not in username_password:
        print("\n\t\tThere is no account associated with this username\n")
        continue
    else:
        # Check if username has been entered
        while USERNAME_ENTERED is True:
            login_password = input("\nPlease enter your password:\n")
            # Apply hashlib to hash the users password
            PASSWORD_HASH = sha256(login_password.encode("utf-8")).hexdigest()
            if username_password[login_username] != PASSWORD_HASH:
                print("\n\t\tThis password is incorrect\n")
                continue
            else:
                print("\n\n\t\tYour login has been successful\n\n")
            logged_in = True
            break


def reg_user():
    """
    Register the user
    If user has added any invalid characters, recur the function
    If user has added a valid username and password, hash the password
    Append username and password to the user.txt file
    """
    username = input("\nPlease input a new username:\n")
    if " " in username:
        print("\n\t\tYour username must not contain any spaces\n")
        reg_user()
    if ";" in username:
        print("\n\t\tYour username must not contain ';'\n")
        reg_user()
    if len(username) < 8:
        print("\n\t\tYour username must be at least 8 characters long\n")
        reg_user()
    if username.lower() in username_password:
        print("\n\t\tThis username is already taken, please choose a different one\n")
        reg_user()
    else:
        while True:
            username = username.lower()
            password = input("\nPlease input a password:\n")
            if " " in password:
                print("\n\t\tYour password must not contain spaces\n")
                continue
            if ";" in password:
                print("\n\t\tYour password must not contain ';'\n")
                continue
            if len(password) < 8:
                print("\n\t\tYour password must be at least 8 characters long\n")
                continue
            while True:
                confirm_password = input("\nPlease confirm your password:\n")
                if password == confirm_password:
                    # Apply the hash method to the comfirmed password
                    hashed_password = sha256(confirm_password.encode())
                    file.append(username, hashed_password, "user.txt")
                    username_password[username] = hashed_password
                    return username_password
                else:
                    print("\n\t\tPasswords do not match\n")
                    continue


def add_task():
    """
    Add a task
    Assign usernames and passwords from user data to dictionary
    If new username isn't in dictionary, recur the function
    Else request for task details
    Append new task to task list
    """
    task_list = []
    user_data = file.read("user.txt").split("\n")
    for i in user_data:
        i = i.split(";")
        username_password[i[0]] = i[1]
    task_username = input(
        "\nPlease input the username of whom the task is assigned to:\n"
    )
    if task_username not in username_password:
        print("\n\t\tThis user does not exist\n")
        add_task()
    else:
        task_title = input("\nPlease input a task title:\n")
        task_description = input("\nPlease input a task description:\n")
        # Request for the task due date in the date format
    while True:
        try:
            task_due_date = input("\nDue date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        # Show an error if the user enters an invalid date format
        except ValueError:
            print("\n\t\tInvalid datetime format. Please use the format specified:\n")
            continue

    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False,
    }

    # Append new task to tasks.txt file
    task_list.append(new_task)
    with open("tasks.txt", "a+", encoding="utf-8") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t["username"],
                t["title"],
                t["description"],
                t["due_date"].strftime(DATETIME_STRING_FORMAT),
                t["assigned_date"].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t["completed"] else "No",
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
        task_file.write("\n")
    print("\n\t\tTask successfully added\n")
    main()


def view_all(tasks):
    """
    View all tasks
    Assign tasks in tasks.txt to a dictionary, then add to a list
    Display tasks
    """
    print("\n\t\tTasks:\n")
    for num, task in enumerate(tasks):
        print(
            f"\nTask number: {num +1}\nAssigned to: {task['assigned_to']}\nTask name: {task['task_name']}\nTask description: {task['description']}\nDue date: {task['due_date']}\nDate assigned: {task['date_assigned']}\nCompleted: {task['completed']}\n"
        )


def change_due_date(task, tasks):
    """
    Change the due date of a task
    Display value error if incorrect format is entered and recur the function
    If the correct format is given, call the update tasks function to make changes
    """
    try:
        task["due_date"] = str(input("Due date of task (YYYY-MM-DD): "))
    except ValueError:
        print("\n\t\tInvalid datetime format. Please use the format specified\n")
        change_due_date(task, tasks)
    update_tasks(tasks, task)


def change_completion_status(task, tasks):
    """
    Change completion status of a task
    Request for user input to mark as complete or return to menu
    Display error if incorrect input is given and recur the function
    If correct input is given, call update_tasks function to make changes
    """
    task["completed"] = str(
        input("\nPlease type 'y' to mark the task as complete or 'n' to go back:\n")
    )
    if task["completed"].lower() == "y":
        task["completed"] = "Yes"
        update_tasks(tasks, task)
    if task["completed"].lower() == "n":
        view_mine()
    else:
        print("\n\t\tYour choice has not been recognised\n")
        change_completion_status(task, tasks)


def change_username(task, tasks, user_data):
    """
    Change who the task is assigned to
    Request for a new users name
    While the new users name exists, call update tasks to make changes
    If the new users name is not recognised, recur the function
    """
    total_users = []
    for user in user_data:
        user = user.split(";")
        total_users.append(user[0])
    task["assigned_to"] = str(input("\nPlease input a new user:\n"))
    while task["assigned_to"] in total_users:
        update_tasks(tasks, task)
    print("\n\t\tThis user does not exist\n")
    change_username(task, tasks, user_data)


def update_tasks(tasks, task):
    """
    Apply changes made to specified task
    Print updated task list to a temp file, then change temp_file to tasks.txt
    """
    if task["db_row"] >= 1:
        fetched_rows = [task["db_row"] - 1 for task in tasks]
    elif task["db_row"] < 1:
        fetched_rows = [task["db_row"] for task in tasks]
    try:
        # Open tasks.txt file in read and write mode and open temp.txt file in write mode
        with open("tasks.txt", "r+", encoding="utf-8") as task_file, open(
            "temp.txt", "w", encoding="utf-8"
        ) as temp_file:
            # Loop through task_file and enumerate each line
            for db_row, line in enumerate(task_file):
                if db_row in fetched_rows:
                    # Remove the corresponding row from fetched rows
                    fetched_rows.remove(db_row)
                    # Pop the relevant task out of tasks, slice from 2nd item, join together
                    print(
                        ";".join(v for k, v in list(tasks.pop(0).items())[2:]),
                        file=temp_file,
                    )
                else:
                    print(line.strip(), file=temp_file)
                # Show file not found error if the tasks.txt file is not found
    except FileNotFoundError:
        print("\nThis page is currently down for maintenance\n")
        sys.exit()

    os.remove("tasks.txt")
    os.rename("temp.txt", "tasks.txt")

    print("\n\t\tYour changes to the task have been saved\n")

    main()


def view_mine():
    """
    Display only the logged in users tasks
    Include logic enabling a user to choose how to edit a task
    """
    tasks = []
    i = 0
    # Open the tasks.txt file in read mode
    lines = file.read("tasks.txt").splitlines()
    print("\n\t\tYour tasks: \n")
    for db_row, line in enumerate(lines):
        assigned_to, *rest = line.split(";")
        if login_username == assigned_to:
            # Use a dictionary to display the task fields
            task_data = {
                k: v
                for k, v in zip(
                    (
                        "number",
                        "db_row",
                        "assigned_to",
                        "task_name",
                        "description",
                        "due_date",
                        "date_assigned",
                        "completed",
                    ),
                    (i + 1, db_row + 1, assigned_to, *rest),
                )
            }
            tasks.append(task_data)
            i += 1

            print(
                f"\nTask number: {task_data['number']}\nAssigned to: {task_data['assigned_to']}\nTask name: {task_data['task_name']}\nTask description: {task_data['description']}\nDue date: {task_data['due_date']}\nDate assigned: {task_data['date_assigned']}\nCompleted: {task_data['completed']}\n"
            )

    if len(tasks) == 0:
        print("\nYou don't have any tasks pending\n")
        main()
    else:
        try:
            task_choice = int(
                input(
                    "\nPlease enter the number of a task to edit or type '-1' to go back\n"
                )
            )
        except ValueError:
            print("\n\t\tYou have not entered a number\n")
            view_mine()
        if str(task_choice) == "-1":
            main()
        # Check if users choice is 0 or if number of task does not exist
        if task_choice == 0 or task_choice > (len(tasks)):
            print("\n\t\tYou have entered an incorrect number\n")
            view_mine()
        # Reduce the users task choice number by 1 for it match with the task list items index
        task = tasks[task_choice - 1]
        if task["completed"] == "Yes":
            print("\n\t\tThis task is complete and can no longer be edited\n")
            view_mine()
        editing_complete = False
        while editing_complete is False:
            edit_option = str(
                input(
                    "\nHow would you like to edit this task?\ne - Edit task\nc - Mark as complete\n-1 - Return to the main menu\n"
                )
            )
            # Request from the user what they would like to edit while editing is not complete
            while editing_complete is False:
                if edit_option == "e":
                    edit = str(
                        input(
                            "\nWhat would you like to edit?\nu - Username\nd - Due date\n-1 - Return to the main menu\n"
                        )
                    )
                    if edit.lower() == "u":
                        change_username(task, tasks, user_data)
                    if edit.lower() == "d":
                        change_due_date(task, tasks)
                    if edit == "-1":
                        main()
                    else:
                        print("\n\t\tYour choice has not been recognised")
                        continue
                if edit_option == "c":
                    change_completion_status(task, tasks)
                if edit_option == "-1":
                    main()
                else:
                    print("\n\t\tYour choice has not been recognised")
                    break


# Class for generating reports
class Reports:
    """
    Parent class for generating reports
    Create class variables
    """

    def __init__(self, tasks, task_lines):
        self.curr_date = curr_date
        self.task_lines = task_lines
        self.tasks = tasks


# Class for generating task reports and inheriting from the Reports parent class
class TaskOverview(Reports):
    """
    Generate task reports and inherit from Reports parent class
    Loop through task data and generate statistics
    Create task_overview.txt file to display the task reports
    """

    def __init__(self, tasks, task_lines):
        # Use super initialization to inherit parent arguments
        super().__init__(self, task_lines)
        incomplete_count = 0
        complete_count = 0
        incomp_and_not_due_count = 0
        incomp_and_due_count = 0
        # Assign the number of tasks to a variable
        task_length = len(task_lines)
        # Output a message to the user if there are no tasks
        if task_length == 0:
            print("\t\tThere are no tasks")
            main()
        else:
            for task in tasks:
                due_date = task["due_date"]
                date = datetime.strptime(due_date, "%Y-%m-%d").date()
                # Check if task is completed
                if task["completed"] == "No":
                    incomplete_count += 1
                    # Check if date comes after the current date
                    if date > curr_date:
                        incomp_and_not_due_count += 1
                    # Check if date comes before the current date
                    elif date < curr_date:
                        incomp_and_due_count += 1
                        # Check if task is complete
                elif task["completed"] == "Yes":
                    complete_count += 1

        # Print the statistics to task_overview.txt file
        print(
            "\n\nPlease select the task_overview.txt and user_overview.txt files for Task and User Reports\n\n"
        )

        with open("task_overview.txt", "w", encoding="utf-8") as t:
            t.write("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tTask reports:\n\n\n")
            t.write(f"Total number of tasks: {task_length}\n\n")
            t.write(
                f"Percentage of incomplete tasks: {round(incomplete_count / task_length * 100)} %\n\n"
            )

            t.write(
                f"Percentage of complete tasks: {round(complete_count / task_length * 100)} %\n\n"
            )

            t.write(f"Tasks incomplete and not due: {incomp_and_not_due_count}\n\n")
            t.write(f"Tasks incomplete and overdue: {incomp_and_due_count}\n\n")
            t.write(f"Complete tasks: {complete_count}\n\n")
            t.write(f"Incomplete tasks: {incomplete_count}\n\n")
            t.write(
                f"Percentage of incomplete and not due tasks: {round(incomp_and_not_due_count / task_length * 100)} %\n\n"
            )

            t.write(
                f"Percentage of incomplete and overdue tasks: {round(incomp_and_due_count / task_length * 100)} %\n\n"
            )


class UserOverview(Reports):
    """
    Generate user reports and inherit from Reports parent class
    Loop through user data and task data and count how many instances for each user
    Create user_overview.txt file to display user reports
    """

    def __init__(self, tasks, user_data, task_lines):
        super().__init__(tasks, task_lines)
        task_length = len(task_lines)
        user_counter = {}
        total_users = []
        individual_allocated_percentage = {}
        individual_complete_percentage = {}
        individual_incomplete_percentage = {}
        individual_incomplete_overdue = {}

        for user in user_data:
            user = user.split(";")
            # Append each username to a list
            total_users.append(user[0])

        # Assign the number of total users and total tasks to the dictionary
        user_counter["total_users"] = len(total_users)
        user_counter["total_tasks"] = task_length

        for user in total_users:
            # Create a dictionary for each user
            user_counter[user] = dict()
            for task in tasks:
                # Check if the user is in the task dictionary
                if task["assigned_to"] == user:
                    # Add an increment of 1 to 'total' for this user
                    user_counter[user]["total"] = user_counter[user].get("total", 0) + 1
                    if task["completed"] == "Yes":
                        # Add an increment of 1 to 'completed' for this user
                        user_counter[user]["completed"] = (
                            user_counter[user].get("completed", 0) + 1
                        )
                    elif task["completed"] == "No":
                        # Add 1 to 'to_be_completed' for this user
                        user_counter[user]["to_be_completed"] = (
                            user_counter[user].get("to_be_completed", 0) + 1
                        )
                        # Format the task due date with datetime
                        date_due = datetime.strptime(
                            task["due_date"], "%Y-%m-%d"
                        ).date()
                        # Check if the due date has already passed
                        if date_due < curr_date:
                            user_counter[user]["overdue"] = (
                                user_counter[user].get("overdue", 0) + 1
                            )

        for user in total_users:
            if user in user_counter:
                # Get the user totals for total tasks and total completed tasks
                individual_allocated_percentage[user] = user_counter[user].get("total")
                individual_complete_percentage[user] = user_counter[user].get(
                    "completed"
                )

                # Get the user totals for tasks to be completed
                individual_incomplete_percentage[user] = user_counter[user].get(
                    "to_be_completed"
                )

                # Get the user totals for incomplete and overdue tasks
                individual_incomplete_overdue[user] = user_counter[user].get("overdue")
                individual_incomplete_overdue[user] = (
                    individual_incomplete_overdue[user] or 0
                )
                # Get the user totals for allocated tasks
                individual_allocated_percentage[user] = (
                    individual_allocated_percentage[user] or 0
                )
                # Get the user totals for complete tasks
                individual_complete_percentage[user] = (
                    individual_complete_percentage[user] or 0
                )
                # Get the user totals for incomplete tasks
                individual_incomplete_percentage[user] = (
                    individual_incomplete_percentage[user] or 0
                )

            # If users task list is not equal to 0, calculate percentage of allocated tasks
            if task_length != 0:
                individual_allocated_percentage[user] = round(
                    individual_allocated_percentage[user] / task_length * 100
                )
            else:
                individual_allocated_percentage[user] = 0

            # If users task list is not equal to 0, calculate percentage of complete tasks
            if individual_allocated_percentage[user] != 0:
                individual_complete_percentage[user] = round(
                    individual_complete_percentage[user]
                    / individual_allocated_percentage[user]
                    * 100
                )
            else:
                individual_complete_percentage[user] = 0

            # If users task list is not equal to 0, calculate percentage of incomplete tasks
            if individual_allocated_percentage[user] != 0:
                individual_incomplete_percentage[user] = round(
                    user_counter[user].get("to_be_completed", 0)
                    / individual_incomplete_percentage[user]
                    * 100
                )
            else:
                individual_incomplete_percentage[user] = 0
            # If users task list is not equal to 0, calculate percentage of incomplete and overdue tasks
            if individual_allocated_percentage[user] != 0:
                individual_incomplete_overdue[user] = round(
                    individual_incomplete_overdue[user]
                    / individual_allocated_percentage[user]
                    * 100
                )
            else:
                individual_incomplete_overdue[user] = 0

        # Print the statistics to user_overview.txt file

        with open("user_overview.txt", "w", encoding="utf-8") as t:
            t.write("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tUser reports:\n\n\n")
            t.write(
                f"The total number of users registered with task_manager: {len(total_users)}\n\n"
            )

            t.write(f"\n\nTotal number of tasks: {task_length}\n\n")

            t.write("\n\n\t\tPercentage of allocated tasks per user:\n")
            for key, value in individual_allocated_percentage.items():
                t.write(f"\n{key}: {value} %\n")

            t.write("\n\n\t\tPercentage of completed tasks per user:\n")
            for key, value in individual_complete_percentage.items():
                t.write(f"\n{key}: {value} %\n")

            t.write("\n\n\t\tPercentage of incomplete tasks per user:\n")
            for key, value in individual_incomplete_percentage.items():
                t.write(f"\n{key}: {value} %\n")

            t.write("\n\n\t\tPercentage of incomplete and overdue tasks per user:\n")
            for key, value in individual_incomplete_overdue.items():
                t.write(f"\n{key}: {value} %\n")


def read_data(va_selected):
    """
    Read data from tasks.txt and user.txt
    If the user has selected view_all from menu,
    Call the view_all function and pass in tasks
    Call the TaskOverview and UserOverview classes and pass in data
    """
    task_lines = file.read("tasks.txt").splitlines()
    tasks = []
    i = 0
    for db_row, line in enumerate(task_lines):
        assigned_to, *rest = line.split(";")
        task_data = {
            k: v
            for k, v in zip(
                (
                    "number",
                    "db_row",
                    "assigned_to",
                    "task_name",
                    "description",
                    "due_date",
                    "date_assigned",
                    "completed",
                ),
                (i + 1, db_row, assigned_to, *rest),
            )
        }
        tasks.append(task_data)

    if va_selected is True:
        view_all(tasks)
    else:
        user_data = file.read("user.txt").split("\n")

        # Create instances of the TaskOverview and UserOverview class
        TaskOverview(tasks, task_lines)
        UserOverview(tasks, user_data, task_lines)


def main():
    """
    Display menu that is specific to either admin or standard user
    Call functions dependent on user input choice
    """
    while True:
        print("\n\t\tMenu:\n")
        if login_username.lower() == "admin":
            print(
                "'r'.  Register\n'a'.  Add a task \n'va'. View all tasks \n'vm'. View my tasks\n'gr'. Generate reports\n'ds'. Display statistics\n'e'   Exit"
            )
        else:
            print(
                "'a'.  Add a task \n'va'. View all tasks \n'vm'. View my tasks\n'e'.  Exit\n"
            )
        choice = input("\nPlease enter the revelent letter from the menu:\n\n")
        if choice.lower() == "r":
            reg_user()
        if choice.lower() == "a":
            add_task()
        if choice.lower() == "va":
            va_selected = True
            read_data(va_selected)
        if choice.lower() == "vm":
            view_mine()
        if login_username.lower() == "admin" and choice.lower() == "gr":
            va_selected = False
            read_data(va_selected)
        if choice.lower() == "e":
            print("\n\t\tThank you for using the Task Manager\n\n")
            exit()


main()
