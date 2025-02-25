import sqlite3 # Will be used to connect to the database
import cgi # Will be used to parse the form data from the HTML
import os 

def initialize_db():
    """
    This function initializes the database if it does not exist.
    """
    conn = sqlite3.connect('polling_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS crimes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        count INTEGER,
        feeling_safe TEXT
    )''')

    conn.commit()
    conn.close()


def process_input():
    """
    This function processes the form data and inserts it into the database.
    """
    form = cgi.FieldStorage() # Parse the form data (https://docs.python.org/3/library/cgi.html)
    crime_type = form.getvalue('crime_type')
    crime_count = form.getvalue('crime_count')
    feeling_safe = form.getvalue('feeling_safe') or 'No' # Default to 'No' if not provided

    conn = sqlite3.connect('polling_data.db')
    c = conn.cursor()
    c.execute('INSERT INTO crimes (type, count, feeling_safe) VALUES (?, ?, ?)', (crime_type, crime_count, feeling_safe))
    conn.commit()
    conn.close()

    print("Content-type: text/html\n") # Required header
    print("<html><body><h2>Data Submitted!</h2><a href='index.html'>Go Back</a></body></html>")


if __name__ == "__main__":
    if not os.path.exists("polling_data.db"): # If the database does not exist, initialize it
        initialize_db()
