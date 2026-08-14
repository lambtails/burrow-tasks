from flask import Flask, render_template, request
import sqlite3

if __name__ == "__main__":
    # Create database connection
    connect = sqlite3.connect("database.db")
    connect.execute("""
		CREATE TABLE IF NOT EXISTS tasks (
		description TEXT NOT NULL,
		done BOOL NOT NULL,
		archived BOOL NOT NULL
		)
		""")

    # Start flask app and define URL routes
    app = Flask(__name__)

    @app.route("/", methods=["GET", "POST"])
    def index():
        if request.method == "POST":
            # Add new task to the database!
            description = request.form["description"]
            with sqlite3.connect("database.db") as users:
                cursor = users.cursor()
                cursor.execute(
                    """
					INSERT INTO tasks \
						(description,done,archived) VALUES (?,?,?)
					""",
                    (description, False, False),
                )
                users.commit()

            # Redirect to a GET request so the browser doesn't redo stuff
            app.redirect(app.url_for("success"))

        # Connect and load database for GET request
        connect = sqlite3.connect("database.db")
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM tasks")
        data = cursor.fetchall()
        connect.close()

        # Render webpage
        return render_template("index.html", data=data)

    @app.route("/success")
    def success():
        app.redirect(app.url_for("index"))

    app.run(debug=False)
