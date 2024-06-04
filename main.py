# Importing the necessary libraries
from cs50 import SQL
import helper
import os
from werkzeug.security import generate_password_hash, check_password_hash
from getpass4 import getpass
from prettytable import PrettyTable


def create_database():
    """Creates the database file."""

    # Checking if the location of the .db file exists
    if not os.path.exists(os.path.join(os.getcwd(), "database.db")):

        # Opening the file in the write mode
        with open(os.path.join(os.getcwd(), "database.db"), "w") as file:
            pass


def init_database(db: SQL):
    """Initializes the database by creating the required tables in the database."""

    db.execute(
        """
        CREATE TABLE IF NOT EXISTS "users" (
            "id"            INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            "username"      TEXT NOT NULL UNIQUE,
            "first_name"    TEXT NOT NULL,
            "last_name"     TEXT NOT NULL,
            "password_hash" TEXT NOT NULL
        );
        """
    )

    db.execute(
        """
        CREATE TABLE IF NOT EXISTS "expenses" (
            "expense_track_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            "user_id"          INTEGER NOT NULL,
            "title"            TEXT NOT NULL,
            "description"      TEXT NOT NULL,
            "date"             TEXT NOT NULL,
            "amount"           NUMERIC NOT NULL
        );
        """
    )


def register(db: SQL):
    """Register function."""

    # Taking input from the user for the username
    username = helper.take_input_as_string(
        "Enter your username: ", "Invalid username. Please try again."
    )

    # Taking input from the user for the first name
    first_name = helper.take_input_as_string(
        "Enter your first name: ", "Invalid first name. Please try again."
    )

    # Taking input from the user for the last name
    last_name = helper.take_input_as_string(
        "Enter your last name: ", "Invalid last name. Please try again."
    )

    # Taking input from the user for the password
    while True:

        # Getting the password using the getpass function
        password = getpass("Enter your password: ")

        # If the password is None
        if password.strip() is None:

            # Printing an error message
            print("Invalid password input! ")

            # Running the loop
            continue

        # If the password is not None
        else:

            # Breaking the loop
            break

    # Try to execute the SQL query
    try:

        # Executing the query
        new_user_id = db.execute(
            "INSERT INTO users (username, first_name, last_name, password_hash) VALUES (?, ?, ?, ?)",
            username,
            first_name,
            last_name,
            generate_password_hash(password),
        )

        # Printing the message
        print("Registered successfully with User ID: {}.".format(new_user_id))

        # Return the function
        return True

    # If the query fails as ValueError or RuntimeError
    except ValueError or RuntimeError:

        # Printing an error message
        print("Registration failed. Please try again.")

        # Returning the function
        return False


def login(db: SQL):
    """Login function"""

    # Taking the input for the username
    username = helper.take_input_as_string("Enter your username: ")

    # Taking the input for the password
    while True:

        # Getting the password using the getpass function
        password = getpass("Enter the password: ")

        # If the password is None
        if password.strip() is None:

            # Printing an error message
            print("Invalid password input! ")

            # Running the loop
            continue

        # If the password is not None
        else:

            # Breaking the loop
            break

    # Checking if the username exists
    users = db.execute(
        """
        SELECT * FROM users 
        WHERE username = ?
        """,
        username,
    )

    # If the length of the query returned is zero
    if len(users) == 0:

        # Printing an error message
        print("No such user found! \n")

        # Returning the function
        return False

    elif check_password_hash(users[0]["password_hash"], password):

        # Printing the message
        print("Successfully Logged In \n")

        # Printing the welcome message
        print(
            "Welcome {} {}!".format(
                str(users[0]["first_name"]).strip(), str(users[0]["last_name"]).strip()
            )
        )

        # Returning the function
        return (True, users[0]["id"])


def add(user_id: int, db: SQL):
    """Function to add an expense."""

    # Taking the input from the user for the title
    title = helper.take_input_as_string("Enter the title: ")

    # Taking the input for the description
    description = input("Enter the description (Optional): ")

    # Taking the input for the amount
    amount = helper.take_input_as_numeric(
        message="Enter the expense amount: ",
        error_message="Invalid amount. Please try again.",
        zero=False,
        decimal_allowed=True,
        negative_allowed=False,
    )

    # Taking the input for the date
    date = input("Enter the date (Optional): ")

    # Inserting the data into the database
    new_task_id = db.execute(
        """
        INSERT INTO expenses (user_id, title, description, date, amount) VALUES (?, ?, ?, ?, ?)
        """,
        user_id,
        title,
        "-" if description is None else description,
        "-" if date is None else date,
        amount,
    )

    # Printing an INFO message
    print("Successfully Added Task: {}".format(new_task_id))

    # Returning the function
    return


def view(user_id: int, db: SQL):
    """Function to view the expenses."""

    # Getting the data from the database
    expenses = db.execute(
        """
        SELECT * FROM expenses 
        WHERE user_id = ? 
        ORDER BY date DESC
        """,
        user_id,
    )

    # If the length of the query returned is zero
    if len(expenses) == 0:

        # Print an error message
        print("No expense found!\n")

        # Returning the function
        return

    # Initializing the PrettyTable
    p = PrettyTable()

    # Setting the field names of the table
    p.field_names = [
        "Serial Number",
        "Task ID",
        "Title",
        "Description",
        "Date",
        "Amount",
    ]

    # Adding the data to the table
    for i, k in enumerate(expenses):

        # Adding the data into the row
        p.add_row(
            [
                i + 1,
                k["expense_track_id"],
                k["title"],
                k["description"],
                k["date"],
                k["amount"],
            ]
        )

    # Print the table
    print(p)

    # Return the function
    return


def edit(user_id: int, db: SQL):
    """Function to edit the expenses."""

    # Same as view functino
    expenses = db.execute(
        """
        SELECT * FROM expenses 
        WHERE user_id = ? 
        ORDER BY date DESC
        """,
        user_id,
    )

    # If the length of the query returned is zero
    if len(expenses) == 0:

        # Print an error message
        print("No expense found!\n")

        # Returning the function
        return

    # Initializing the PrettyTable
    p = PrettyTable()

    # Setting the field names of the table
    p.field_names = [
        "Serial Number",
        "Task ID",
        "Title",
        "Description",
        "Date",
        "Amount",
    ]

    # Adding the data to the table
    for i, k in enumerate(expenses):

        # Adding the data into the row
        p.add_row(
            [
                i + 1,
                k["expense_track_id"],
                k["title"],
                k["description"],
                k["date"],
                k["amount"],
            ]
        )

    # Print the table
    print(p)

    # Getting the input for the serial number
    task_serial_number = helper.input_in_options(
        "Enter the serial number of the expense you want to edit: ",
        [str(i) for i in range(1, len(expenses) + 1)],
    )

    # Getting new values
    new_title = input("Enter the new title (Optional): ")
    new_description = input("Enter the new description (Optional): ")
    new_date = input("Enter the new date (Optional): ")
    new_amount = helper.take_input_as_numeric(
        message="Enter the new expense amount (Please enter again if the amount has not changed): ",
        error_message="Invalid amount. Please try again.",
        zero=False,
        decimal_allowed=True,
        negative_allowed=False,
    )

    # Updating the database
    db.execute(
        """
        UPDATE expenses SET title = ?, description = ?, date = ?, amount = ? WHERE expense_track_id = ?
        """,
        (
            expenses[int(task_serial_number) - 1]["title"]
            if new_title is None
            else new_title
        ),
        (
            expenses[int(task_serial_number) - 1]["description"]
            if new_description is None
            else new_description
        ),
        (
            expenses[int(task_serial_number) - 1]["date"]
            if new_date is None
            else new_date
        ),
        (
            expenses[int(task_serial_number) - 1]["amount"]
            if new_amount is None
            else new_amount
        ),
        expenses[int(task_serial_number) - 1]["expense_track_id"],
    )

    # Print an INFO message
    print(
        "Successfully Updated Task: {}".format(
            expenses[int(task_serial_number) - 1]["expense_track_id"]
        )
    )

    # Returning the function
    return


def delete(user_id: int, db: SQL):
    """Delete Expenses from the database."""

    # Getting the data from the database
    expenses = db.execute(
        """
        SELECT * FROM expenses 
        WHERE user_id = ? 
        ORDER BY date DESC
        """,
        user_id,
    )

    # If the length of the query returned is zero
    if len(expenses) == 0:

        # Print an error message
        print("No expense found!\n")

        # Returning the function
        return

    # Initializing the PrettyTable
    p = PrettyTable()

    # Setting the field names of the table
    p.field_names = [
        "Serial Number",
        "Task ID",
        "Title",
        "Description",
        "Date",
        "Amount",
    ]

    # Adding the data to the table
    for i, k in enumerate(expenses):

        # Adding the data into the row
        p.add_row(
            [
                i + 1,
                k["expense_track_id"],
                k["title"],
                k["description"],
                k["date"],
                k["amount"],
            ]
        )

    # Print the table
    print(p)

    # Getting the serial number of the task to be deleted
    task_serial_number = helper.input_in_options(
        "Enter the serial number of the expense you want to delete: ",
        [str(i) for i in range(1, len(expenses) + 1)],
    )

    # Deleting the data from the database
    db.execute(
        """
        DELETE FROM expenses WHERE expense_track_id = ?
        """,
        expenses[int(task_serial_number) - 1]["expense_track_id"],
    )

    # Print an INFO message
    print("Task Deleted Successfully! ")

    # Returning the function
    return


def main(db: SQL):
    """Main function."""

    # Getting if the user wants to register or login
    user_mode = helper.input_in_options(
        "Enter the mode (Register [R] / Login [L]): ", ["R", "L"]
    )

    # If the user wants to register
    if str(user_mode).upper().strip() == "R":

        # Running the register function
        register(db)

    # If the user wants to log in
    elif str(user_mode).upper().strip() == "L":

        # Running the log in function
        is_log_in_successful = login(db)

        # If the log in function returned False
        if type(is_log_in_successful) == bool:

            # Printing an exiting program
            print("Exiting...")

            # Returning the main function
            return

        # While the log in function returned True

        while True:

            try:
                # If the log in function returned True
                log_in_user_mode = helper.input_in_options(
                    "Enter the mode (Add [A] / View [V] / Edit [E] / Delete [D] / Quit [Q]): ",
                    ["A", "V", "E", "D", "Q"],
                )

                # If the user want to add a new expense
                if str(log_in_user_mode).upper().strip() == "A":

                    # Running the add function with the user id and the SQL object
                    add(is_log_in_successful[1], db)

                elif str(log_in_user_mode).upper().strip() == "V":

                    # Running the view function with the user ID and the SQL object
                    view(is_log_in_successful[1], db)

                elif str(log_in_user_mode).upper().strip() == "E":

                    # Running the edit function with the User ID and the SQL object
                    edit(is_log_in_successful[1], db)

                elif str(log_in_user_mode).upper().strip() == "D":

                    # Running the delete function with the User ID and the SQL object
                    delete(is_log_in_successful[1], db)

                elif str(log_in_user_mode).upper().strip() == "Q":

                    # Printing the exiting message
                    print("Exiting...")

                    # Breaking the function
                    break

            # For Keyboard Interrupt error or EOF error
            except KeyboardInterrupt or EOFError:

                # Continue the loop
                continue

    # Returning the function
    return


# If the program is run as the main program
if __name__ == "__main__":

    # Creates the required database file
    create_database()

    # Creates a SQL Object from the generated database
    db = SQL("sqlite:///database.db")

    # Initializes the database with the above generated SQL object
    init_database(db)

    # Try/Catch block for Keyboard Interrupt
    try:

        # Initialize the main function
        main(db)

    # For Keyboard Interrupt error
    except KeyboardInterrupt:

        # Printing the exit message
        print("Exiting...")
