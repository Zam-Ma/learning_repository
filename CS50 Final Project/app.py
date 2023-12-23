import sqlite3

from flask import Flask, flash, redirect, render_template, request, session, g
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import (
    login_required,
    pln,
    apology,
    get_db,
    createDefaultCategories,
    validate,
    clear,
)
from datetime import datetime

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["pln"] = pln

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.teardown_appcontext
def close_db(error):
    """Close the database at the end of the request."""

    db = g.pop("db", None)
    if db is not None:
        db.close()


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    # User reached route via POST
    if request.method == "POST":
        # Initiate cursor
        db, cursor = get_db()

        # Get values from the form
        title = clear(request.form.get("title"))
        cost = clear(request.form.get("cost"))
        category_id = clear(request.form.get("category_id"))
        date = clear(request.form.get("date"))

        # If values are valid
        if validate(title, cost, category_id, date):
            # Insert values into the database
            cursor.execute(
                "INSERT INTO spendings (user_id, title, category_id, cost, date) VALUES (?, ?, ?, ?, ?)",
                (session["user_id"], title, category_id, cost, date),
            )

            # Commit database entry
            db.commit()

            # Redirect to homepage
            return redirect("/")

        # If values are invalid
        else:
            flash("Wrong input. Please try again")
            return redirect("/")

    # User reached route via GET
    else:
        # Query database for the recent categories and spendings
        db, cursor = get_db()

        categories = cursor.execute(
            "SELECT id, category FROM categories WHERE user_id = ? ORDER BY category",
            (session["user_id"],),
        ).fetchall()

        # Display all spendings
        spendings = cursor.execute(
            "SELECT spendings.id, spendings.title, spendings.cost, categories.category, spendings.date FROM spendings JOIN categories ON spendings.category_id = categories.id WHERE spendings.user_id = ? ORDER BY spendings.date DESC;",
            (session["user_id"],),
        ).fetchall()

        return render_template("index.html", categories=categories, spendings=spendings)


@app.route("/categories", methods=["GET", "POST"])
@login_required
def categories():
    # Show and edit categories

    # User reached route via POST
    if request.method == "POST":
        # Initiate cursor
        db, cursor = get_db()

        # Get values from the form
        newCategory = clear(request.form.get("category"))

        # Add category to the categories database and commit changes
        cursor.execute(
            "INSERT INTO categories (user_id, category) VALUES (?, ?)",
            (session["user_id"], newCategory),
        )
        db.commit()

        # Reload page
        return redirect("/categories")

    # User reached route via GET
    else:
        # Initiate cursor
        db, cursor = get_db()

        # Query database for existing categories and spendings
        categorySpendings = cursor.execute(
            "SELECT categories.id, categories.category, COALESCE(SUM(spendings.cost), 0) AS totalCost FROM categories LEFT JOIN spendings ON spendings.category_id = categories.id AND spendings.user_id = ? WHERE categories.user_id = ? GROUP BY categories.category ORDER BY totalCost DESC",
            (session["user_id"], session["user_id"]),
        ).fetchall()
        return render_template("categories.html", categorySpendings=categorySpendings)


@app.route("/searchCategoriesDates", methods=["POST"])
@login_required
def searchCategoriesDates():
    # Initiate cursor
    db, cursor = get_db()

    # Get values from the form
    dateBegin = request.form.get("dateCategoriesBegin")
    dateEnd = request.form.get("dateCategoriesEnd")

    # If values are valid
    if validate(dateBegin, dateEnd):
        # Query database for the recent categories and spendings
        db, cursor = get_db()

        # If both dateBegin and dateEnd are provided
        if dateBegin and dateEnd:
            categorySpendings = cursor.execute(
                "SELECT categories.id, categories.category, COALESCE(SUM(spendings.cost), 0) AS totalCost FROM categories LEFT JOIN spendings ON spendings.category_id = categories.id AND spendings.user_id = ? WHERE categories.user_id = ? AND spendings.date >= ? AND spendings.date <= ? GROUP BY categories.category ORDER BY totalCost DESC",
                (session["user_id"], session["user_id"], dateBegin, dateEnd),
            ).fetchall()
        # If only dateBegin is provided
        elif dateBegin:
            categorySpendings = cursor.execute(
                "SELECT categories.id, categories.category, COALESCE(SUM(spendings.cost), 0) AS totalCost FROM categories LEFT JOIN spendings ON spendings.category_id = categories.id AND spendings.user_id = ? WHERE categories.user_id = ? AND spendings.date >= ? GROUP BY categories.category ORDER BY totalCost DESC",
                (session["user_id"], session["user_id"], dateBegin),
            ).fetchall()
        # If only dateEnd is provided
        elif dateEnd:
            categorySpendings = cursor.execute(
                "SELECT categories.id, categories.category, COALESCE(SUM(spendings.cost), 0) AS totalCost FROM categories LEFT JOIN spendings ON spendings.category_id = categories.id AND spendings.user_id = ? WHERE categories.user_id = ? AND spendings.date <= ? GROUP BY categories.category ORDER BY totalCost DESC",
                (session["user_id"], session["user_id"], dateEnd),
            ).fetchall()
        # If neither dateBegin nor dateEnd is provided
        else:
            categorySpendings = cursor.execute(
                "SELECT categories.id, categories.category, COALESCE(SUM(spendings.cost), 0) AS totalCost FROM categories LEFT JOIN spendings ON spendings.category_id = categories.id AND spendings.user_id = ? WHERE categories.user_id = ? GROUP BY categories.category ORDER BY totalCost DESC",
                (session["user_id"], session["user_id"]),
            ).fetchall()
        return render_template("categories.html", categorySpendings=categorySpendings)

    # If values are invalid
    else:
        flash("Wrong input. Please try again")
        return redirect("/")


@app.route("/editCategoryName", methods=["POST"])
@login_required
def editCategoryName():
    # Initiate cursor
    db, cursor = get_db()

    # Get values from the form
    category_id = request.form.get("category_id")
    new_category_name = clear(request.form.get("edit_category_name"))

    # If values are valid
    if validate(new_category_name):
        # Update database row
        cursor.execute(
            "UPDATE categories SET category = ? WHERE id = ?",
            (new_category_name, category_id),
        )
        db.commit()

        # Reload page
        return redirect("/categories")

    # If values are invalid
    else:
        flash("Wrong input. Please try again")
        return redirect("/categories")


@app.route("/deleteCategory", methods=["POST"])
@login_required
def deleteCategory():
    # Initiate cursor
    db, cursor = get_db()

    # Get category_id from the form
    category_id = request.form.get("category_id")

    # If the User doesn't try deleting 'No category' category
    if category_id != "No category":
        # Change all deelted category spendings categories to 'No category'
        cursor.execute(
            "UPDATE spendings SET category_id = (SELECT id FROM categories WHERE category = 'No category' AND user_id = ?) WHERE category_id = ? LIMIT 1",
            (session["user_id"], category_id),
        )
        # Delete the category
        cursor.execute(
            "DELETE FROM categories WHERE id = ?",
            (category_id,),
        )
        db.commit()

        # Reload page
        return redirect("/categories")


@app.route("/searchDates", methods=["POST"])
@login_required
def searchDates():
    # Initiate cursor
    db, cursor = get_db()

    # Get values from the form
    dateBegin = request.form.get("dateBegin")
    dateEnd = request.form.get("dateEnd")

    # If values are valid
    if validate(dateBegin, dateEnd):
        # Query database for the recent categories and spendings
        db, cursor = get_db()

        categories = cursor.execute(
            "SELECT id, category FROM categories WHERE user_id = ? ORDER BY category",
            (session["user_id"],),
        ).fetchall()

        # If both dateBegin and dateEnd are provided
        if dateBegin and dateEnd:
            spendings = cursor.execute(
                "SELECT spendings.id, spendings.title, spendings.cost, categories.category, spendings.date FROM spendings JOIN categories ON spendings.category_id = categories.id WHERE spendings.user_id = ? AND spendings.date BETWEEN ? AND ? ORDER BY spendings.date DESC;",
                (session["user_id"], dateBegin, dateEnd),
            ).fetchall()
        # If only dateBegin is provided
        elif dateBegin:
            spendings = cursor.execute(
                "SELECT spendings.id, spendings.title, spendings.cost, categories.category, spendings.date FROM spendings JOIN categories ON spendings.category_id = categories.id WHERE spendings.user_id = ? AND spendings.date >= ? ORDER BY spendings.date DESC;",
                (session["user_id"], dateBegin),
            ).fetchall()
        # If only dateEnd is provided
        elif dateEnd:
            spendings = cursor.execute(
                "SELECT spendings.id, spendings.title, spendings.cost, categories.category, spendings.date FROM spendings JOIN categories ON spendings.category_id = categories.id WHERE spendings.user_id = ? AND spendings.date <= ? ORDER BY spendings.date DESC;",
                (session["user_id"], dateEnd),
            ).fetchall()
        # If neither dateBegin nor dateEnd is provided
        else:
            spendings = cursor.execute(
                "SELECT spendings.id, spendings.title, spendings.cost, categories.category, spendings.date FROM spendings JOIN categories ON spendings.category_id = categories.id WHERE spendings.user_id = ? ORDER BY spendings.date DESC;",
                (session["user_id"],),
            ).fetchall()

        return render_template("index.html", categories=categories, spendings=spendings)

    # If values are invalid
    else:
        flash("Wrong input. Please try again")
        return redirect("/")


@app.route("/editRow", methods=["POST"])
@login_required
def editRow():
    # Initiate cursor
    db, cursor = get_db()

    # Get values from the form
    id = request.form.get("edit_id")
    title = request.form.get("edit_title")
    cost = request.form.get("edit_cost")
    category_id = request.form.get("edit_category_id")
    date = request.form.get("edit_date")
    print(id, title, cost, category_id, date)


    # If values are valid
    if validate(title, cost, category_id, date):
        # Update database row
        cursor.execute(
            "UPDATE spendings SET title = ?, category_id = ?, cost = ?, date = ? WHERE id = ?",
            (title, category_id, cost, date, id),
        )
        db.commit()

        # Reload page
        return redirect("/")

    # If values are invalid
    else:
        flash("Wrong input. Please try again")
        return redirect("/")


@app.route("/deleteRow", methods=["POST"])
@login_required
def deleteRow():
    # Initiate cursor
    db, cursor = get_db()

    # Get id from the form
    id = clear(request.form.get("id"))

    # Delete row from the database and commit database change
    cursor.execute(
        "DELETE FROM spendings WHERE id = ?",
        (id,),
    )
    db.commit()

    # Reload page
    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Please enter username")
            return render_template("login.html")

        # Ensure password was submitted
        if not request.form.get("password"):
            flash("Please enter password")
            return render_template("login.html")

        # Query database for username
        db, cursor = get_db()

        username = clear(request.form.get("username"))
        password = clear(request.form.get("password"))

        userCheck = cursor.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        # Ensure username exists and password is correct
        if userCheck is None or not check_password_hash(userCheck["hash"], password):
            flash("Invalid username and/or password. Please try again.")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = userCheck["id"]

        # Redirect user to home page
        flash("Logged in!")
        return redirect("/")

    # User reached route via GET
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST
    if request.method == "POST":
        username = clear(request.form.get("username"))
        password = clear(request.form.get("password"))
        confirmation = clear(request.form.get("confirmation"))

        # Ensure username was submitted
        if not username:
            flash("Please enter username.")
            return render_template("register.html")

        # Ensure password  was submitted
        if not password:
            flash("Please enter password.")
            return render_template("register.html")

        # Ensure password confirmation was submitted
        if not confirmation:
            flash("Please enter password confirmation.")
            return render_template("register.html")

        # Ensure password and confirmation match
        if password != confirmation:
            flash("Passwords do not match. Please try again.")

        # Ensure username is not already taken
        db, cursor = get_db()
        userCheck = cursor.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        )
        if userCheck.fetchone() is not None:
            flash("User already exists. Please try different username.")
            return render_template("register.html")

        # Register user into the database
        cursor.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)",
            (username, generate_password_hash(password)),
        )

        # Commit changes to the database
        db.commit()

        # Remember which user has logged in
        user_id = cursor.execute(
            "SELECT id FROM users WHERE username = ?", (username,)
        ).fetchone()
        session["user_id"] = user_id["id"]

        # Create default categories for the user
        createDefaultCategories(user_id["id"], db, cursor)

        # Redirect user to home page
        flash("Registered!")
        return redirect("/")

    # User reached route via GET
    else:
        return render_template("register.html")
