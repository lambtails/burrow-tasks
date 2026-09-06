from flask import Flask, render_template, request
from werkzeug.middleware.proxy_fix import ProxyFix
import sqlite3
import datetime

# Create database connection
db = "database.db"
detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
list_names = ["burrow", "puppy", "bunny"]

# Generate a table if none exists
with sqlite3.connect(db, detect_types=detect_types) as connect:
    connect.execute("""
        CREATE TABLE IF NOT EXISTS Tasks (
        RowID INTEGER NOT NULL PRIMARY KEY,
        Description TEXT NOT NULL,
        List TEXT NOT NULL,
        Done BOOL NOT NULL,
        Archived BOOL NOT NULL,
        CreationDate TIMESTAMP,
        DoneDate TIMESTAMP,
        ArchiveDate TIMESTAMP
        );
        """)

# Start flask app and define URL routes
app = Flask(__name__, static_folder="static")
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)


@app.route("/", methods=["GET"])
def index():
    # Get list name from query string
    list_name = request.args.get("l", default=list_names[0], type=str)
    if list_name not in list_names:
        list_name = list_names[0]

    # Connect and load database for GET request
    with sqlite3.connect(db, detect_types=detect_types) as connect:
        cursor = connect.cursor()
        cursor.execute(
            """
            SELECT *
            FROM Tasks
            WHERE Archived=False AND List=?
            ORDER BY Done ASC, DoneDate DESC, CreationDate ASC;
            """,
            (list_name,),
        )
        data = cursor.fetchall()
        cursor.execute("""
            SELECT List, COUNT(*)
            FROM Tasks
            WHERE Archived=False
            GROUP BY List;
            """)
        counts = cursor.fetchall()
        cursor.close()

    # Render webpage
    return render_template(
        "index.html", data=data, counts=counts, list_name=list_name, tabs=list_names
    )


@app.route("/add", methods=["POST"])
def add():
    # Get list name from form data and make sure it's valid
    list_name: str | None = request.form.get("list_name")
    if list_name not in list_names:
        list_name = list_names[0]

    # Get task description and datetime
    description: str | None = request.form.get("description")
    current_datetime = datetime.datetime.now()

    # Add a new task to the database
    if description is not None:
        with sqlite3.connect(db, detect_types=detect_types) as connect:
            cursor = connect.cursor()
            cursor.execute(
                """
                INSERT INTO Tasks (Description,List,Done,Archived,CreationDate) 
                VALUES (?,?,?,?,?);
                """,
                (description, list_name, False, False, current_datetime),
            )
            connect.commit()
            cursor.close()

    # Return to index page
    return app.redirect(app.url_for(endpoint="index", l=list_name))


@app.route("/clear", methods=["POST"])
def clear():
    # Get list name from form data and make sure it's valid
    list_name: str | None = request.form.get(
        "list_name", default=list_names[0], type=str
    )
    if list_name not in list_names:
        list_name = list_names[0]

    # Get datetime
    current_datetime = datetime.datetime.now()

    # Archive completed tasks in the list
    with sqlite3.connect(db, detect_types=detect_types) as connect:
        cursor = connect.cursor()
        cursor.execute(
            """
            UPDATE Tasks
            SET Archived=?, ArchiveDate=?
            WHERE Done=?;
            """,
            (True, current_datetime, True),
        )
        connect.commit()
        cursor.close()

    # Return to index page
    return app.redirect(app.url_for(endpoint="index", l=list_name))


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

    # Return empty string
    return ""


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
