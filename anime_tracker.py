import sqlite3

# Connect to the database
con = sqlite3.connect("anime_tracker.db")
cur = con.cursor()

# Create the table if it doesn't already exist
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


def add_anime():
    title = input("Enter anime title: ")
    genre = input("Enter genre: ")
    rating = int(input("Enter rating (out of 10): "))
    status = input("Enter status (Watching, Completed, Plan to Watch, Dropped): ")
    episodes_watched = int(input("Enter episodes watched: "))
    date_started = input("Enter date started (YYYY-MM-DD): ")
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

    if len(rows) == 0:
        print("No anime found.")
    else:
        print("\n--- All Anime ---")
        for row in rows:
            print(row)


def search_anime():
    search_title = input("Enter title to search for: ")

    cur.execute("SELECT * FROM anime WHERE title LIKE ?", ('%' + search_title + '%',))
    rows = cur.fetchall()

    if len(rows) == 0:
        print("No matching anime found.")
    else:
        print("\n--- Search Results ---")
        for row in rows:
            print(row)


def update_anime():
    anime_id = int(input("Enter the id of the anime you want to update: "))

    cur.execute("SELECT * FROM anime WHERE id = ?", (anime_id,))
    anime = cur.fetchone()

    if anime is None:
        print("Anime not found.")
        return

    print("\nCurrent record:")
    print(anime)

    new_title = input("Enter new title: ")
    new_genre = input("Enter new genre: ")
    new_rating = int(input("Enter new rating: "))
    new_status = input("Enter new status: ")
    new_episodes_watched = int(input("Enter new episodes watched: "))
    new_date_started = input("Enter new date started: ")
    new_notes = input("Enter new notes: ")

    cur.execute("""
        UPDATE anime
        SET title = ?, genre = ?, rating = ?, status = ?, episodes_watched = ?, date_started = ?, notes = ?
        WHERE id = ?
    """, (new_title, new_genre, new_rating, new_status, new_episodes_watched, new_date_started, new_notes, anime_id))

    con.commit()
    print("Anime updated successfully!")


def delete_anime():
    anime_id = int(input("Enter the id of the anime you want to delete: "))

    cur.execute("SELECT * FROM anime WHERE id = ?", (anime_id,))
    anime = cur.fetchone()

    if anime is None:
        print("Anime not found.")
        return

    print("\nRecord to be deleted:")
    print(anime)

    confirm = input("Are you sure you want to delete this anime? (yes/no): ")

    if confirm.lower() == "yes":
        cur.execute("DELETE FROM anime WHERE id = ?", (anime_id,))
        con.commit()
        print("Anime deleted successfully!")
    else:
        print("Delete canceled.")


def main():
    while True:
        print("\n--- Anime Tracker ---")
        print("1. Add anime")
        print("2. View all anime")
        print("3. Search anime by title")
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
            print("Invalid choice. Please try again.")


main()
con.close()
