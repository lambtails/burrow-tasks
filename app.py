from flask import Flask, render_template, request
import sqlite3

# Create database connection
db = "database.db"
connect = sqlite3.connect(db)
connect.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
    rowid INTEGER NOT NULL PRIMARY KEY,
    description TEXT NOT NULL,
    done BOOL NOT NULL,
    archived BOOL NOT NULL,
    deleted BOOL NOT NULL
    )
    """)

# Start flask app and define URL routes
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Add new task to the database!
        description = request.form.get("description")
        with sqlite3.connect(db) as users:
            cursor = users.cursor()
            cursor.execute(
                """
                INSERT INTO tasks \
                    (description,done,archived,deleted) VALUES (?,?,?,?)
                """,
                (description, False, False, False),
            )
            users.commit()

        # Redirect to a GET request so the browser doesn't redo stuff
        return app.redirect(app.url_for(endpoint="index"))

    # Connect and load database for GET request
    connect = sqlite3.connect(db)
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM tasks")
    data = cursor.fetchall()
    connect.close()

    # Render webpage
    return render_template("index.html", data=data)


@app.route("/update", methods=["POST"])
def update():
    # Get data from the JSON request
    rowid: int = int(request.json.get("rowid"))
    done: bool | None = request.json.get("done")

    # Update the database
    connect = sqlite3.connect(db)
    cursor = connect.cursor()
    cursor.execute(
        """
        UPDATE tasks \
        SET done=? \
        WHERE rowid=?
        """,
        (done, rowid),
    )
    connect.commit()
    connect.close()

    # Return empty string for now
    return ""


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')
