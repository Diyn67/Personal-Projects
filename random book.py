import random

def read_file(file_path):
    """Reads the file and returns a list of book entries (as tuples or strings)."""
    try:
        with open(file_path, 'r') as file:
            books = []
            for line in file:
                line = line.strip()
                if " - " in line:  # Check if the entry includes an author
                    title, author = line.split(" - ", 1)
                    books.append((title, author))
                else:  # Only a title
                    books.append(line)
            return books
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return []

def write_file(file_path, data):
    """Writes the list of data to the file, handling entries with or without authors."""
    with open(file_path, 'w') as file:
        for entry in data:
            if isinstance(entry, tuple):  # If it's a tuple (title, author)
                title, author = entry
                file.write(f"{title} - {author}\n")
            else:  # If it's a single string (only title)
                file.write(f"{entry}\n")

def normalize_entry(title, author=None):
    """Formats a book entry as a tuple or string depending on whether an author is provided."""
    if author and author.strip():
        return (title.strip(), author.strip())
    return title.strip()

def get_random_book(file_path):
    """Selects a random book from the file, handling empty lists gracefully."""
    books = read_file(file_path)
    if books:
        return random.choice(books)
    else:
        print(f"No books available in {file_path}.")
        return None

def move_book(book, source_file, destination_file):
    """Moves a book from the source file to the destination file, ensuring no duplicates across files."""
    source_books = read_file(source_file)
    destination_books = read_file(destination_file)

    if book in source_books:
        if book in destination_books:
            print(f"'{book}' already exists in {destination_file}. Cannot move.")
        else:
            source_books.remove(book)
            write_file(source_file, source_books)
            
            destination_books.append(book)
            write_file(destination_file, destination_books)
            print(f"Moved '{book}' from {source_file} to {destination_file}.")
    else:
        print(f"Book '{book}' not found in {source_file}.")

def add_book(title, author, file_path):
    """Adds a book with title and optional author to the specified file."""
    book_entry = normalize_entry(title, author)
    books = read_file(file_path)
    if book_entry not in books:
        books.append(book_entry)
        write_file(file_path, books)
        print(f"Added '{title}' to {file_path}.")
    else:
        print(f"'{title}' already exists in {file_path}.")

def get_random_from_multiple_files(file_paths):
    """Selects a random book from multiple files."""
    all_books = []
    for file_path in file_paths:
        all_books.extend(read_file(file_path))
    if all_books:
        return random.choice(all_books)
    else:
        print("No books available in the specified files.")
        return None

def main():
    tbr_file = 'TBR.txt'
    finished_file = 'Finished.txt'
    read_again_file = 'ReadAgain.txt'
    did_not_like_file = 'DidNotLike.txt'

    while True:
        print("\nMenu:")
        print("1. Add a new book to TBR")
        print("2. Get a random book from TBR")
        print("3. Mark a book as Finished")
        print("4. Move a book to Read Again")
        print("5. Move a book to Did Not Like")
        print("6. Get a random book from TBR and Read Again")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            title = input("Enter the book title: ").strip()
            author = input("Enter the author's name (leave blank if unknown): ").strip()
            if not author:
                author = None
            add_book(title, author, tbr_file)
        elif choice == '2':
            book = get_random_book(tbr_file)
            if book:
                if isinstance(book, tuple):
                    print(f"Random Book: {book[0]} by {book[1]}")
                else:
                    print(f"Random Book: {book}")
        elif choice == '3':
            title = input("Enter the book title: ").strip()
            author = input("Enter the author's name (leave blank if unknown): ").strip()
            book = normalize_entry(title, author if author else None)
            move_book(book, tbr_file, finished_file)
            add_to_read_again = input("Do you want to add this book to the Read Again list? (yes/no): ").strip().lower()
            if add_to_read_again == 'yes':
                add_book(title, author, read_again_file)
        elif choice == '4':
            title = input("Enter the book title: ").strip()
            author = input("Enter the author's name (leave blank if unknown): ").strip()
            book = normalize_entry(title, author if author else None)
            move_book(book, finished_file, read_again_file)
        elif choice == '5':
            title = input("Enter the book title: ").strip()
            author = input("Enter the author's name (leave blank if unknown): ").strip()
            book = normalize_entry(title, author if author else None)
            move_book(book, tbr_file, did_not_like_file)
            move_book(book, finished_file, did_not_like_file)
        elif choice == '6':
            book = get_random_from_multiple_files([tbr_file, read_again_file])
            if book:
                if isinstance(book, tuple):
                    print(f"Random Book: {book[0]} by {book[1]}")
                else:
                    print(f"Random Book: {book}")
        elif choice == '7':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()