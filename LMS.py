from datetime import datetime


class Library:
    admins = {"admin": "admin"}
    borrowers = {}
    available_books = {}
    borrowing_history = {}


class Admin:
    def __init__(self) -> None:
        self.logged_in = False

    def create_admin(self, username, password):
        if self.logged_in:
            Library.admins[username] = password

    def create_borrower(self, borrower_details):
        if self.logged_in:
            Borrower().register(*borrower_details)

    def login(self, username, password):
        if username in Library.admins and Library.admins[username] == password:
            self.logged_in = True

    def add_book(
        self,
        book_title,
        author_name,
        total_pages,
        no_of_copies_available,
        isbn,
        published_year,
    ):
        if self.logged_in:
            for book_details in Library.available_books.values():
                if isbn == book_details["isbn"]:
                    print(
                        "Adding Book Failed - Book with the entered ISBN is already in the Library"
                    )
                    return
            book_id = (
                1
                if len(Library.available_books) == 0
                else max(Library.available_books.keys()) + 1
            )
            Library.available_books[book_id] = {
                "title": book_title,
                "author_name": author_name,
                "total_pages": total_pages,
                "no_of_copies_available": int(no_of_copies_available),
                "isbn": isbn,
                "published_year": published_year,
            }

    def edit_book(
        self,
        book_id,
        book_title,
        author_name,
        total_pages,
        no_of_copies_available,
        isbn,
        published_year,
    ):
        if self.logged_in:
            if book_id in Library.available_books:
                book = Library.available_books[book_id]
                Library.available_books[book_id] = {
                    "title": book_title if book_title.strip() != "" else book["title"],
                    "author_name": (
                        author_name
                        if author_name.strip() != ""
                        else book["author_name"]
                    ),
                    "total_pages": (
                        total_pages
                        if total_pages.strip() != ""
                        else book["total_pages"]
                    ),
                    "no_of_copies_available": (
                        int(no_of_copies_available)
                        if no_of_copies_available.strip() != ""
                        else book["no_of_copies_available"]
                    ),
                    "isbn": isbn if isbn.strip() != "" else book["isbn"],
                    "published_year": (
                        published_year
                        if published_year.strip() != ""
                        else book["published_year"]
                    ),
                }
                print("Book details updated successfully")
            else:
                print("Book with the entered ID not found")

    def delete_book(self, delete_book_id):
        if self.logged_in:
            if delete_book_id in Library.available_books:
                Library.available_books.pop(delete_book_id)
                print("Book deleted successfully")
            else:
                print("Book with the entered ID not found")

    def view_book_details_and_borrowing_history(self, book_id):
        if self.logged_in:
            if book_id not in Library.available_books:
                print("No book is available with the given book ID")
                return
            book = Library.available_books[book_id]
            print("\n------ Book Details ------")
            print("Book Title:", book["title"])
            print("Author Name:", book["author_name"])
            print("Total Pages:", book["total_pages"])
            print("No. of copies available:", book["no_of_copies_available"])
            print("IBSN:", book["isbn"])
            print("Published Year:", book["published_year"])
            is_borrowing_history_available = False
            print("----- Borrowing History -----")
            for borrower_email, borrowing_history in Library.borrowing_history.items():
                for book_history in borrowing_history:
                    if book_id == book_history["book_id"]:
                        is_borrowing_history_available = True
                        print("Borrower Email: ", borrower_email)
                        print(
                            "Borrowed Date:",
                            book_history["borrowed_date"],
                        )
                        print(
                            "Returned Date:",
                            book_history["returned_date"],
                        )
                        print("Fine:", book_history["fine"])
                        print("-" * 25)
            if not is_borrowing_history_available:
                print("No borrowing history")

    def list_borrowers_and_borrowing_history(self):
        if self.logged_in:
            for borrower_email, borrower_details in Library.borrowers.items():
                print("\n------ Borrower ------")
                print("Full Name:", borrower_details["full_name"])
                print("DOB:", borrower_details["dob"])
                print("Contact Number:", borrower_details["contact_no"])
                print("Email:", borrower_email)
                print("Password:", borrower_details["password"])
                print("----- Borrowed Books -----")
                if borrower_email not in Library.borrowing_history:
                    print("No borrowing history found")
                    continue
                for borrowing_history in Library.borrowing_history[borrower_email]:
                    print("Book ID:", borrowing_history["book_id"])
                    print("Borrowed Date:", borrowing_history["borrowed_date"])
                    print("Returned Date:", borrowing_history["returned_date"])
                    print("Fine:", borrowing_history["fine"])
                    print("-" * 25)

    def give_book(self, book_id, borrower_email):

        if book_id not in Library.available_books:
            print("No book with the given book id is found")
            return

        if borrower_email not in Library.borrowers:
            print("No borrowers with the given email is found")
            return

        remaining_copies = Library.available_books[book_id]["no_of_copies_available"]
        if remaining_copies == 0:
            print("Giving Book Failed - No more book copies left")
            return

        if borrower_email in Library.borrowing_history:
            for book_details in Library.borrowing_history[borrower_email]:
                if (
                    book_id == book_details["book_id"]
                    and book_details["returned_date"] == ""
                ):
                    print(
                        "Giving Book Failed - Book with the given id is currently borrowed"
                    )
                    return
        else:
            Library.borrowing_history[borrower_email] = []

        borrowing_details = {
            "book_id": book_id,
            "borrowed_date": str(datetime.now().date()),
            "returned_date": "",
            "fine": "",
        }
        Library.borrowing_history[borrower_email].append(borrowing_details)
        Library.available_books[book_id]["no_of_copies_available"] -= 1
        print("Book is given to the borrower successfully")

    def accept_book_return(self, book_id, borrower_email):

        if book_id not in Library.available_books:
            print("No book with the given book id is found in the Library")
            return

        if borrower_email not in Library.borrowers:
            print("No borrower with the given email is found in the accounts")
            return

        if borrower_email not in Library.borrowing_history:
            print("No borrowing history is found for the given borrower email")
            return
        else:
            for book_details in Library.borrowing_history[borrower_email]:
                if (
                    book_id == book_details["book_id"]
                    and book_details["returned_date"] == ""
                ):
                    borrowed_date = datetime.strptime(
                        book_details["borrowed_date"], "%Y-%m-%d"
                    )
                    returned_date = datetime.now()
                    if (returned_date - borrowed_date).days > 15:
                        book_details["fine"] = "100 INR"
                        print("Fine of INR 100 is charged for the late return")
                    book_details["returned_date"] = str(returned_date.date())
                    Library.available_books[book_id]["no_of_copies_available"] += 1
                    print("Book is returned succcessfully")
                    return
            print(
                "Book with the given id is either returned already or never borrowed by the borrower"
            )
            return


class Borrower:
    def __init__(self) -> None:
        self.logged_in = False
        self.full_name = None
        self.dob = None
        self.contact_no = None
        self.email = None
        self.password = None

    def login(self, username, password):
        if (
            username in Library.borrowers
            and Library.borrowers[username]["password"] == password
        ):
            self.logged_in = True

            # Load Data
            self.full_name = Library.borrowers[username]["full_name"]
            self.dob = Library.borrowers[username]["dob"]
            self.contact_no = Library.borrowers[username]["contact_no"]
            self.email = username
            self.password = password

    def register(self, full_name, dob, contact_no, email, password):
        if email not in Library.borrowers:
            if email and password:
                Library.borrowers[email] = {
                    "full_name": full_name,
                    "dob": dob,
                    "contact_no": contact_no,
                    "password": password,
                }
                print("Registered borrower successfully!")
            else:
                print("Registration failed. Email and Password cannot be empty.")
        else:
            print("Registration failed. Email already exists.")

    def view_currently_borrowed_books(self):
        if self.logged_in:
            if self.email not in Library.borrowing_history:
                print("No books have been borrowed yet")
                return
            max_days = 15
            today = datetime.now()
            for borrowing_history in Library.borrowing_history[self.email]:
                if borrowing_history["returned_date"] == "":
                    print("-" * 25)
                    print("Book ID:", borrowing_history["book_id"])
                    print("Borrowed Date:", borrowing_history["borrowed_date"])
                    borrowed_date = datetime.strptime(
                        borrowing_history["borrowed_date"], "%Y-%m-%d"
                    )
                    days_gone = (today - borrowed_date).days
                    remaining_days = max_days - days_gone
                    print(
                        "Remaining Days:", remaining_days if remaining_days > 0 else 0
                    )
                    print("-" * 25)
                    break
            else:
                print("No currently borrowed books")

    def view_book_details_of_each_borrowed_book(self):
        if self.logged_in:
            if self.email not in Library.borrowing_history:
                print("No books have been borrowed yet")
                return
            for borrowing_history in Library.borrowing_history[self.email]:
                book_id = borrowing_history["book_id"]
                print("-" * 25)
                print("Book ID:", book_id)
                if book_id not in Library.available_books:
                    print(
                        "No book details found in library. (Possible case of deleted book)"
                    )
                    continue
                book = Library.available_books[book_id]
                print("Book Title:", book["title"])
                print("Author Name:", book["author_name"])
                print("Total Pages:", book["total_pages"])
                print("No. of copies available:", book["no_of_copies_available"])
                print("IBSN:", book["isbn"])
                print("Published Year:", book["published_year"])
            print("-" * 25)

    def view_borrowing_history(self):
        if self.logged_in:
            if self.email not in Library.borrowing_history:
                print("No books have been borrowed yet")
                return
            for borrowing_history in Library.borrowing_history[self.email]:
                print("-" * 25)
                print("Book ID:", borrowing_history["book_id"])
                print("Borrowed Date:", borrowing_history["borrowed_date"])
                print("Returned Date:", borrowing_history["returned_date"])
                print("Fine:", borrowing_history["fine"])
            print("-" * 25)


def get_borrower_details_to_register():
    full_name = input("Full Name: ")
    dob = input("DOB: ")
    contact_no = input("Contact Number: ")
    email = input("Email: ")
    password = input("Password: ")

    return (
        full_name,
        dob,
        contact_no,
        email,
        password,
    )


def get_book_details_to_add_or_edit():
    book_title = input("Book Title: ")
    author_name = input("Author Name: ")
    total_pages = input("Total Pages: ")
    no_of_copies_available = input("No. of copies available in the library: ")
    isbn = input("ISBN: ")
    published_year = input("Published Year: ")

    return (
        book_title,
        author_name,
        total_pages,
        no_of_copies_available,
        isbn,
        published_year,
    )


def handle_admin_operations(admin: Admin, operation_no):
    if operation_no == 1:
        print("To create a new admin, enter the following details")
        username = input("Username: ")
        password = input("Password: ")
        admin.create_admin(username, password)
    elif operation_no == 2:
        print("To create borrower, enter the following details")
        admin.create_borrower(get_borrower_details_to_register())
    elif operation_no == 3:
        print("To add a new book, enter the following details")
        admin.add_book(*get_book_details_to_add_or_edit())
    elif operation_no == 4:
        print("To edit a book, enter the following details")
        edit_book_id = int(input("Book ID: "))
        print("To leave the field with previous value, just press enter to skip")
        admin.edit_book(edit_book_id, *get_book_details_to_add_or_edit())
    elif operation_no == 5:
        print("To delete a book, enter the following details")
        delete_book_id = int(input("Book ID: "))
        admin.delete_book(delete_book_id)
    elif operation_no == 6:
        print("To view book details and borrowing history, enter the following details")
        book_id = int(input("Book ID: "))
        admin.view_book_details_and_borrowing_history(book_id)
    elif operation_no == 7:
        print("Listing all borrowers details and their borrowing history")
        admin.list_borrowers_and_borrowing_history()
    elif operation_no == 8:
        print("To give book to the borrower, enter the following details")
        book_id = int(input("Book ID: "))
        borrower_email = input("Borrower email: ")
        admin.give_book(book_id, borrower_email)
    elif operation_no == 9:
        print("To accept book return, enter the following details")
        book_id = int(input("Book ID: "))
        borrower_email = input("Borrower email: ")
        admin.accept_book_return(book_id, borrower_email)
    elif operation_no == 10:
        admin.logged_in = False
        print("Logged out succesfully!")
    else:
        print("Invalid operation")


def handle_borrower_operations(borrower: Borrower, operation_no):
    if operation_no == 1:
        print("Viewing the currently borrowed books")
        borrower.view_currently_borrowed_books()
    elif operation_no == 2:
        print("Viewing the book details of each borrowed book")
        borrower.view_book_details_of_each_borrowed_book()
    elif operation_no == 3:
        print("Viewing the borrowing history")
        borrower.view_borrowing_history()
    elif operation_no == 4:
        borrower.logged_in = False
        print("Logged out successfully!")
    else:
        print("Invalid operation")


def main():
    print("+-------------------------------+")
    print("|   Library Management System   |")
    print("+-------------------------------+")
    library_opened = True
    while library_opened:
        print("\n\tLogin as\t\tRegister as")
        print("1. Admin   2. Borrower   (or)   3. Borrower   4. Exit Library")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            username = input("Username: ")
            password = input("Password: ")
            admin = Admin()
            admin.login(username, password)
            if admin.logged_in:
                print(f"Welcome {username}! Logged in successfully as admin.")
                while admin.logged_in:
                    print("\n1. Create Admin  2. Create Borrower")
                    print("3. Add Book  4. Edit book  5. Delete Book  6. View Book")
                    print("7. List all borrowers and borrowing history")
                    print("8. Give Book  9. Accept book return  10. Logout")
                    operation_no = int(input("Enter your choice: "))
                    print()
                    handle_admin_operations(admin, operation_no)
            else:
                print("Login Failed. Either username or password is incorrect !")
        elif choice == 2:
            username = input("Username: ")
            password = input("Password: ")
            borrower = Borrower()
            borrower.login(username, password)
            if borrower.logged_in:
                print(
                    f"Welcome {Library.borrowers[username]['full_name']}! Logged in successfully as borrower."
                )
                while borrower.logged_in:
                    print("\n1. View list of currently borrowed books")
                    print("2. View book details of each borrowed book")
                    print("3. View borrowing history  4. Logout")
                    operation_no = int(input("Enter your choice: "))
                    print()
                    handle_borrower_operations(borrower, operation_no)
            else:
                print("Login Failed. Either username or password is incorrect !")
        elif choice == 3:
            print("To register as borrower, please enter the following information")
            Borrower().register(*get_borrower_details_to_register())
        elif choice == 4:
            library_opened = False
            print("Exited from the library. Have a nice day!")
        else:
            print("Invalid operation")


if __name__ == "__main__":
    main()