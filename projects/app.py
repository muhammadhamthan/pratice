from flask import Flask, render_template, request, redirect, session, url_for
import json
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key"

# ------------------ EXPENSE UTILS ------------------
def load_expenses():
    try:
        with open("expenses.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_expenses(expenses):
    with open("expenses.json", "w") as f:
        json.dump(expenses, f, indent=4)

# ------------------ USER UTILS ------------------
def load_users():
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)

# ------------------ ROUTES ------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    users = load_users()
    username = request.form["username"]
    password = request.form["password"]

    if username in users:
        return "Username already exists."
    users[username] = generate_password_hash(password)
    save_users(users)
    return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    users = load_users()
    username = request.form["username"]
    password = request.form["password"]

    if username in users and check_password_hash(users[username], password):
        session["user"] = username
        return redirect("/home")
    return "Invalid credentials"

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

@app.route("/home")
def home():
    if "user" not in session:
        return redirect("/")
    expenses = load_expenses()
    return render_template("home.html", expenses=expenses)

@app.route("/add", methods=["GET", "POST"])
def add():
    if "user" not in session:
        return redirect("/")
    if request.method == "POST":
        new_expense = {
            "date": request.form["date"],
            "category": request.form["category"],
            "amount": float(request.form["amount"]),
            "description": request.form["description"]
        }
        expenses = load_expenses()
        expenses.append(new_expense)
        save_expenses(expenses)
        return redirect("/home")
    return render_template("add_expense.html")

if __name__ == '__main__':
    app.run(debug=True)