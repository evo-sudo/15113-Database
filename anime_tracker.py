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


# Test the function once
add_anime()

# Close connection
con.close()