import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    purchases = db.execute("SELECT * FROM buyers where buyer_id = ?", session["user_id"])
    cash = db.execute("SELECT cash FROM users WHERE id = ?",session["user_id"] )
    cash = cash[0]["cash"]
    totinv = db.execute("SELECT sum(total) as tot FROM buyers WHERE buyer_id = ?",session["user_id"] )
    totinv = totinv[0]["tot"]
    total = cash
    if totinv != None:
        total = cash + totinv
    return render_template("index.html",purchases=purchases, cash=cash, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "GET":
        return render_template("buy.html")

    elif request.method == "POST":
        symb = request.form.get("symbol")
        shares = request.form.get("shares")
        shares = int(shares)
        data = lookup(symb)
        price = data["price"]
        cash = db.execute("SELECT cash FROM users WHERE id = ?",session["user_id"] )
        cash = cash[0]["cash"]
        total = shares * price

        if not data :
            return apology("symbol does not exist", 403)
        elif shares <= 0:
            return apology("please provide a positive number of shares", 403)
        else:
            if shares * price > cash:
                return apology("not enough $$$", 403)
            else:
                cash = cash - (shares * price)
                db.execute("UPDATE users SET cash = ? WHERE id = ?" ,cash , session["user_id"])
                db.execute("INSERT INTO buyers (buyer_id, symbol, name, shares, price, date, time, total) VALUES(?,?,?,?,?,DATE('now'), TIME('now'),?)", session["user_id"], symb, data["name"], shares, price, total)
                db.execute("INSERT INTO transactions (transaction_id, symbol, name, shares, price, type, date, time, total) VALUES(?,?,?,?,?,'buy',DATE('now'), TIME('now'),?)", session["user_id"], symb, data["name"], shares, price, total)

    return redirect("/")



@app.route("/history")
@login_required
def history():
    transactions = db.execute("SELECT * FROM transactions where transaction_id = ?", session["user_id"])
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "GET":
        return render_template("quote.html")
    if request.method == "POST":
        symb = request.form.get("symbol")
        data = lookup(symb)

        if not data :
            return apology("symbol does not exist", 403)
        else:
            data["price"] = usd(data["price"])
            return render_template("quoted.html",data=data)


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        username =request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        hashed = generate_password_hash(password)
        existing = []
        users = db.execute("SELECT username FROM users WHERE username = ?", username)
        for user in users:
            existing.append(user["username"])
        if not username:
            return apology("must provide username", 403)
        elif username in existing :
            return apology("username already exists", 403)
        elif not password:
            return apology("must provide password", 403)
        elif password != confirmation:
            return apology("password not confirmed", 403)
        else:
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hashed)
            userid = db.execute("SELECT id FROM users WHERE username = ?", username)
            session["user_id"] = userid[0]["id"]
            return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    stocks = db.execute("SELECT DISTINCT symbol FROM buyers")
    symbols = []
    for stock in stocks:
        symbols.append(stock["symbol"])
    print(symbols)
    if request.method == "GET":
        return render_template("sell.html", symbols=symbols)
    if request.method == "POST":
        selected = request.form.get("symbol")

        data = lookup(selected)
        curprice = data["price"]

        numberofshares = request.form.get("shares")
        try:
            numberofshares = int(numberofshares)
        except ValueError:
            return apology("please enter a valid number", 403)
        sold = numberofshares

        sharesavail = db.execute("SELECT sum(shares) as summ FROM buyers WHERE symbol = ? and buyer_id = ?", selected, session["user_id"])
        sharesavail = sharesavail[0]["summ"]

        tosell = db.execute("SELECT * FROM buyers WHERE symbol = ? and buyer_id = ?", selected, session["user_id"])
        name =tosell[0]["name"]

        cash = db.execute("SELECT cash FROM users WHERE id = ?",session["user_id"] )
        cash = cash[0]["cash"]

        total = curprice * sold
        cash = cash + total

        if selected not in symbols:
            return apology("sorry stock not found", 403)

        if numberofshares < 0 or numberofshares > sharesavail:
            return apology("please enter a valid number of stocks")

        while numberofshares > 0 :
            for stock in tosell:
                id = stock["id"]
                shares = stock["shares"]
                if shares <= numberofshares:
                    db.execute("DELETE FROM buyers WHERE ID = ?", id)
                    numberofshares -= shares

                elif shares > numberofshares :
                    shares -= numberofshares
                    db.execute("UPDATE buyers SET shares = ? WHERE id = ?",shares ,id)
                    numberofshares-=numberofshares

        db.execute("UPDATE users SET cash = ? WHERE id = ?" ,cash , session["user_id"])
        db.execute("INSERT INTO transactions (transaction_id, symbol, name, shares, price,type , date, time, total) VALUES(?,?,?,?,?, 'sell', DATE('now'), TIME('now'),?)", session["user_id"], selected, name, sold, curprice, total)
        return redirect("/")






