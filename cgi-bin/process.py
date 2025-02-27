import sqlite3 # Will be used to connect to the database
import cgi # Will be used to parse the form data from the HTML
import os 
import pandas as pd
import plotly.express as px

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



def display_data():
    """
    This function displays the data in the database and generates visualizations.
    """
    conn = sqlite3.connect('polling_data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM crimes')
    rows = c.fetchall()
    conn.close()

    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(rows, columns=['ID', 'Crime Type', 'Crime Count', 'Feeling Safe'])

    # Create a bar chart for crime counts
    fig = px.bar(df, x='Crime Type', y='Crime Count', title='Crime Counts by Type')
    fig.write_html("static/crime_counts.html")

    # Create a bar chart for feeling safe
    fig2 = px.bar(df, x='Crime Type', y=df['Feeling Safe'].astype(str), title='Feeling Safe by Crime Type')
    fig2.write_html("static/feeling_safe.html")
    # Display the data and charts
    print("Content-type: text/html\n") # Required header
    print("""
    <html>
    <head>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 40px;
            }
            h2 {
                color: #333;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 20px;
            }
            table, th, td {
                border: 1px solid #ddd;
            }
            th, td {
                padding: 8px;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
            }
            tr:nth-child(even) {
                background-color: #f9f9f9;
            }
            embed {
                display: block;
                margin: 20px 0;
            }
        </style>
    </head>
    <body>
        <h2>Data in the Database</h2>
        <table>
            <tr><th>ID</th><th>Crime Type</th><th>Crime Count</th><th>Feeling Safe</th></tr>""")
    for row in rows:
        print("<tr>")
        for col in row:
            print("<td>{}</td>".format(col))
        print("</tr>")
    print("""
        </table>
        <h2>Crime Counts by Type</h2>
        <embed src='/static/crime_counts.html' width='600' height='400'></embed>
        <h2>Feeling Safe by Crime Type</h2>
        <embed src='/static/feeling_safe.html' width='600' height='400'></embed>
    </body>
    </html>
    """)


if __name__ == "__main__":
    if not os.path.exists("polling_data.db"): # If the database does not exist, initialize it
        initialize_db()
    process_input() # Process the form data and insert it into the database
    display_data() # Display the data in the database



# INSTRUCTIONS:

# python -m http.server 8080 --cgi
# Browse to --> http://localhost:8080/form.html
# Fill out the form and submit
# Use DBBrowser to view the data in the database

# To run local server so that the form can be submitted




# Also now thinking, why the fuck have I been thinking in python... we can just connect to a database.. like a csv or anything...... with javascript and do it like that highkeybikekey bro.

