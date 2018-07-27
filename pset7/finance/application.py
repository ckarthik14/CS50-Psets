import os


from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from time import sleep

from helpers import apology, login_required, lookup, usd


# API_KEY: FEZQRI69L2T14I0I
# export API_KEY=FEZQRI69L2T14I0I
# Ensure environment variable is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd
app.jinja_env.globals.update(usd=usd)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    uid = session.get("user_id")

    # retrieves stock details from database
    cash = db.execute("SELECT cash FROM users WHERE id = :uid", uid=uid)
    portfolio = db.execute("SELECT * FROM portfolio WHERE id = :uid", uid=uid)
    add = cash[0]['cash']
    value = {}

    # retrieves each record for a particular stock

    for record in portfolio:
        comp = record['company']


        while True:
            look = lookup(comp)
            if look == None:
                sleep(2)
                continue
            value[comp] = look['price']
            break

        add += value[comp] * record['stocks']

    return render_template("index.html", cash=usd(cash[0]['cash']),
                           portfolio=portfolio, value=value, add=usd(add))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":
        symbol = request.form.get("symbol")

        while True:
            company = lookup(symbol)
            if company == None:
                sleep(2)
                continue
            break

        shares = request.form.get("shares")

        # check for valid entry in form submission
        if company == None:
            return apology("Enter valid stock name")

        if not shares.isdigit() or int(shares) < 1 or shares == None:
            return apology("Enter valid share amount")

        uid = session.get("user_id")
        query = db.execute("SELECT username FROM users WHERE id = :uid", uid=uid)
        uname = query[0]['username']

        cash = db.execute("SELECT cash FROM users WHERE id = :userid", userid=uid)
        total_price = company['price'] * float(shares)
        comp = company['symbol']
        price = company['price']

        # checks if enough cash is there to purchase the stock
        if cash[0]['cash'] > total_price:
            res = db.execute("SELECT * FROM portfolio WHERE id = :uid AND company = :comp",
                             uid=uid, comp=comp)

            if len(res) == 0:

                db.execute("INSERT INTO portfolio (id, company, stocks) VALUES  \
                (:uid, :company, :stocks)", uid=uid, company=comp, stocks=shares)

            else:
                db.execute("UPDATE portfolio SET stocks = :stocks WHERE \
                id = :uid AND company = :comp", stocks=int(shares) + res[0]['stocks'], uid=uid,
                           comp=comp)

            db.execute("UPDATE users SET cash = cash - :total WHERE id = :uid",
                       uid=uid, total=total_price)
            db.execute("INSERT INTO history (id, company, stocks, price) VALUES (:uid, :company, \
            :stocks, :price)", uid=uid, company=comp, stocks=shares, price=price)

        else:
            return apology("Not enough cash left for your request")

        sleep(1)
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    uid = session.get("user_id")

    # gets history from a separate table for listing
    history = db.execute("SELECT * FROM history WHERE id = :uid", uid=uid)

    return render_template("history.html", history=history)


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

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
    """Get stock quote."""

    if request.method == "POST":
        qte = lookup(request.form.get("symbol"))

        if qte == None:
            return apology("INVALID REQUEST")

        else:
            return render_template("quoted.html", qte=qte)

    else:
        return render_template("quote.html")


@app.route("/reset", methods=["GET", "POST"])
@login_required
def reset():
    """Resets Password"""

    if request.method == "POST":

        oldpass = request.form.get("oldpass")
        newpass = request.form.get("newpass")
        uid = session.get("user_id")

        if not oldpass:
            return apology("Enter old password")

        if not newpass:
            return apology("Enter new password")

        row = db.execute("SELECT * FROM users WHERE id = :uid", uid=uid)
        oldhash = row[0]['hash']
        newhash = generate_password_hash(newpass)

        # checks if old password matches for verification
        if not check_password_hash(oldhash, oldpass):
            return apology("Passwords don't match")

        db.execute("UPDATE users SET hash = :newhash WHERE id = :uid", newhash=newhash, uid=uid)

        sleep(1)
        return redirect("/")

    else:
        return render_template("reset.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    session.clear()

    if request.method == "POST":

        name = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirmation")

        if not name:
            return apology("Username Required")

        if not password:
            return apology("Password Required")

        if not confirm:
            return apology("Confirmation Required")

        if password != confirm:
            return apology("Passwords not matching")

        passhash = generate_password_hash(password)

        result = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=name, hash=passhash)
        if not result:
            return apology("User already exits")

        return redirect("/")

    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":

        symbol = request.form.get("symbol")

        if symbol == None:
            return apology("Select stock")

        shares = request.form.get("shares")

        if not shares.isdigit() or int(shares) < 1 or shares == None:
            return apology("Enter valid share amount")

        while True:
            company = lookup(symbol)
            if company == None:
                sleep(2)
                continue
            break

        uid = session.get("user_id")
        query = db.execute("SELECT username FROM users WHERE id = :uid", uid=uid)
        uname = query[0]['username']

        cash = db.execute("SELECT cash FROM users WHERE id = :userid", userid=uid)
        comp = request.form.get("symbol")

        res = db.execute("SELECT * FROM portfolio WHERE id = :uid AND company = :comp",
                         uid=uid, comp=comp)

        if res[0]['stocks'] >= int(shares):

            price = company['price']
            total_price = company['price'] * float(shares)
            db.execute("UPDATE portfolio SET stocks = :stocks WHERE \
            id = :uid AND company = :comp", stocks=res[0]['stocks'] - int(shares), uid=uid,
                       comp=comp)

            db.execute("UPDATE users SET cash = cash + :total WHERE id = :uid",
                       uid=uid, total=total_price)
            db.execute("INSERT INTO history (id, company, stocks, price) VALUES (:uid, :company, \
            :stocks, :price)", uid=uid, company=comp, stocks=int(shares) * -1, price=price)

        else:
            return apology("Not enough shares with you")

        sleep(1)
        return redirect("/")

    else:
        uid = session.get("user_id")
        query = db.execute("SELECT * FROM portfolio WHERE id = :uid", uid=uid)
        companies = []

        for company in query:
            companies.append(company['company'])

        return render_template("sell.html", companies=companies)


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
