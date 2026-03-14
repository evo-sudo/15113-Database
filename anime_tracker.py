import sqlite3
from datetime import datetime

# Connect to database
con = sqlite3.connect("anime_tracker.db")
cur = con.cursor()

# Create table if it doesn't exist
cur.execute("""
CREATE TABLE IF NOT EXISTS anime (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    genre TEXT,
    rating INTEGER,
    status TEXT,
    episodes_watched INTEGER,
    date_started TEXT,
    notes TEXT
)
""")
con.commit()


# ---------- Input Validation Helpers ----------

def get_int(prompt, min_value=None, max_value=None):
    while True:
        try:
            value = int(input(prompt))

            if min_value is not None and value < min_value:
                print("Value is too small.")
                continue

            if max_value is not None and value > max_value:
                print("Value is too large.")
                continue

            return value

        except ValueError:
            print("Invalid input. Please enter a number.")


def get_date(prompt):
    while True:
        date_input = input(prompt)
        try:
            datetime.strptime(date_input, "%Y-%m-%d")
            return date_input
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")


# ---------- Display Helper ----------

def print_anime(row):
    print("\n----------------------------")
    print(f"ID: {row[0]}")
    print(f"Title: {row[1]}")
    print(f"Genre: {row[2]}")
    print(f"Rating: {row[3]}")
    print(f"Status: {row[4]}")
    print(f"Episodes Watched: {row[5]}")
    print(f"Date Started: {row[6]}")
    print(f"Notes: {row[7]}")
    print("----------------------------")


# ---------- CRUD FUNCTIONS ----------

def add_anime():
    while True:
        title = input("Enter anime title: ").strip()
        if title == "":
            print("Title cannot be empty.")
        else:
            break

    genre = input("Enter genre: ")

    rating = get_int("Enter rating (1-10): ", 1, 10)

    status = input("Enter status (Watching, Completed, Plan to Watch, Dropped): ")

    episodes_watched = get_int("Enter episodes watched: ", 0)

    date_started = get_date("Enter date started (YYYY-MM-DD): ")

    notes = input("Enter notes: ")

    cur.execute("""
    INSERT INTO anime (title, genre, rating, status, episodes_watched, date_started, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (title, genre, rating, status, episodes_watched, date_started, notes))

    con.commit()
    print("Anime added successfully!")


def view_all_anime():
    cur.execute("SELECT * FROM anime")
    rows = cur.fetchall()

    if not rows:
        print("No anime found.")
        return

    print("\n--- All Anime ---")
    for row in rows:
        print_anime(row)


def search_anime():
    title = input("Enter title to search: ")

    cur.execute("SELECT * FROM anime WHERE title LIKE ?", ('%' + title + '%',))
    rows = cur.fetchall()

    if not rows:
        print("No matching anime found.")
        return

    print("\n--- Search Results ---")
    for row in rows:
        print_anime(row)


def update_anime():
    anime_id = get_int("Enter the ID of the anime to update: ")

    cur.execute("SELECT * FROM anime WHERE id = ?", (anime_id,))
    row = cur.fetchone()

    if row is None:
        print("Anime not found.")
        return

    print("\nCurrent Record:")
    print_anime(row)

    new_title = input("Enter new title: ")
    new_genre = input("Enter new genre: ")
    new_rating = get_int("Enter new rating (1-10): ", 1, 10)
    new_status = input("Enter new status: ")
    new_episodes = get_int("Enter new episodes watched: ", 0)
    new_date = get_date("Enter new date started (YYYY-MM-DD): ")
    new_notes = input("Enter new notes: ")

    cur.execute("""
    UPDATE anime
    SET title=?, genre=?, rating=?, status=?, episodes_watched=?, date_started=?, notes=?
    WHERE id=?
    """, (new_title, new_genre, new_rating, new_status, new_episodes, new_date, new_notes, anime_id))

    con.commit()
    print("Anime updated successfully!")


def delete_anime():
    anime_id = get_int("Enter ID of anime to delete: ")

    cur.execute("SELECT * FROM anime WHERE id = ?", (anime_id,))
    row = cur.fetchone()

    if row is None:
        print("Anime not found.")
        return

    print("\nRecord to delete:")
    print_anime(row)

    confirm = input("Are you sure? (yes/no): ")

    if confirm.lower() == "yes":
        cur.execute("DELETE FROM anime WHERE id = ?", (anime_id,))
        con.commit()
        print("Anime deleted.")
    else:
        print("Deletion cancelled.")


# ---------- MAIN MENU ----------

def main():
    while True:
        print("\n=== Anime Tracker ===")
        print("1. Add anime")
        print("2. View all anime")
        print("3. Search anime")
        print("4. Update anime")
        print("5. Delete anime")
        print("6. Quit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_anime()
        elif choice == "2":
            view_all_anime()
        elif choice == "3":
            search_anime()
        elif choice == "4":
            update_anime()
        elif choice == "5":
            delete_anime()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


# Run program
main()

con.close()
