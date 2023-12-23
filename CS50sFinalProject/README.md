# Portphel Expense Tracker

#### Video Demo:  [Watch the Demo](https://youtu.be/EngE9yjUDyw)

#### Description:

Portphel is a web application built with Flask that helps users keep track of their expenses. Users can log in, add, edit, and delete expenses, as well as manage expense categories. The application provides a user-friendly interface for managing financial transactions efficiently.
I've designed this app to help me and my wife manage our finances. I've constructed the database where each user have their own spendings and categories based on their ID.
I've purposely made the menu very basic, so the User doesn't wonder around looking for buttons to press.
Both index and categories UI look very similar: First the User sees add button for either new spendings entry or new category, then - a date filter, and then the table itself.

### app.py
Core routes for my HTML are defined here. I'm quering the SQLite database and outputing it for the user into the HTML.

### helpers.py
A few functions are defined to help out running the core of the program:
- *login_required(f)* decoreates routes to require login.
- *pln(value)* saves as a format function for price output - set to show Polish currency.
- *apology(message, code=400)* - renders an error message
- *get_db()* - function that gets sqlite3 database cursor. I decided not to go with cs50's sqlite3 module, because I wanted to understand basic sqlite3 module
- *createDefaultCategories(user_id, db, cursor) - each registered user gets a list of default categories initialized in the database for him
- *validate(*args)* - function serves as input validator for each of POST submissions through HTML.
- *clear(string)* - replaces '--' inpuyt with '-' to prevent SQL injection.


## Table of Contents

- [Features](#features)
- [Usage](#usage)
- [Dependencies](#dependencies)

## Features

- **User authentication:** Register, log in, and log out securely.
- **Expense tracking:** Add, edit, and delete expenses with details such as title, cost, category, and date.
- **Category management:** Create, edit, and delete expense categories.
- **Filtering:** Filter expenses based on date ranges and categories.
- **Responsive design:** User-friendly interface accessible on various devices.

## Usage

1. Register a new account or log in if you already have one.
2. Start adding your expenses and managing categories.
3. Explore different features, such as filtering expenses based on date ranges or categories.
4. Log out when you're done.

## Dependencies

- Flask
- Flask-Session
- Werkzeug

These dependencies are listed in the `requirements.txt`
