from flask import Flask, render_template, request
import sqlite3
import datetime

# Create database connection
db = "database.db"
detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES

# Generate a table if none exists
with sqlite3.connect(db, detect_types=detect_types) as connect:
    connect.execute("""
        CREATE TABLE IF NOT EXISTS Tasks (
        RowID INTEGER NOT NULL PRIMARY KEY,
        Description TEXT NOT NULL,
        Done BOOL NOT NULL,
        Archived BOOL NOT NULL,
        CreationDate TIMESTAMP,
        DoneDate TIMESTAMP,
        ArchiveDate TIMESTAMP
        );
        """)

# Start flask app and define URL routes
app = Flask(__name__, static_folder="static")


@app.route("/", methods=["GET"])
def index():
    # Connect and load database for GET request
    with sqlite3.connect(db, detect_types=detect_types) as connect:
        cursor = connect.cursor()
        cursor.execute("""
            SELECT *
            FROM Tasks
            WHERE Archived=False
            ORDER BY Done ASC, DoneDate DESC, CreationDate ASC;
            """)
        data = cursor.fetchall()
        cursor.close()

    # Render webpage
    return render_template("index.html", data=data)


@app.route("/add", methods=["POST"])
def add():
    # Get task description and datetime
    description: str | None = request.form.get("description")
    current_datetime = datetime.datetime.now()

    # Add a new task to the database
    if description is not None:
        with sqlite3.connect(db, detect_types=detect_types) as connect:
            cursor = connect.cursor()
            cursor.execute(
                """
                INSERT INTO Tasks (Description,Done,Archived,CreationDate) 
                VALUES (?,?,?,?);
                """,
                (description, False, False, current_datetime),
            )
            connect.commit()
            cursor.close()

    # Return to index page
    return app.redirect(app.url_for(endpoint="index"))


@app.route("/clear", methods=["POST"])
def clear():
    # Get datetime
    archive_date = datetime.datetime.now()

    # Archive completed tasks in the list
    with sqlite3.connect(db, detect_types=detect_types) as connect:
        cursor = connect.cursor()
        cursor.execute(
            """
            UPDATE Tasks
            SET Archived=?, ArchiveDate=?
            WHERE Done=?;
            """,
            (True, archive_date, True),
        )
        connect.commit()
        cursor.close()

    # Return to index page
    return app.redirect(app.url_for(endpoint="index"))


@app.route("/update", methods=["POST"])
def update():
    # Get data from the JSON request
    row_id: int = int(request.json.get("row_id"))
    done: bool | None = request.json.get("done")
    done_date: datetime.datetime | None = (
        datetime.datetime.now() if done == True else None
    )

    # Update the database
    with sqlite3.connect(db, detect_types=detect_types) as connect:
        cursor = connect.cursor()
        cursor.execute(
            """
            UPDATE Tasks
            SET Done=?, DoneDate=?
            WHERE RowID=?;
            """,
            (done, done_date, row_id),
        )
        connect.commit()
        cursor.close()

    # Return empty string for now
    return ""


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
