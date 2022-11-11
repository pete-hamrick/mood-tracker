from flask import Flask, render_template, request, session, redirect
from flask_session import Session
from sqlite3 import Error, connect, Row
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

DATABASE = 'tracker.db'

# consider making an helpers file for this to live in
def get_db_connection():
    connection = None
    try:
        connection = connect(DATABASE)
    except Error as e:
        print(f"the error '{e}' has occured")

    return connection

@app.route("/")
def index():
    return "hello, welcome to the home page"
    # TODO make index.html
    # return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    # POST method
    if request.method == "POST":

        userEmail = request.form.get("email")
        userPassword = request.form.get("password")

        # handle if the user doesn't input an email or password
        if not userEmail or not userPassword:
            message = "Please enter your registered email and password"
            return render_template("login.html", messege=message)
        
        # connect to the database
        con = get_db_connection()

        with con:
            con.row_factory = Row

            cursor = con.cursor()

            # find user in the database by their email
            cursor.execute("SELECT * FROM users WHERE email = ?", (userEmail,))
            rows = cursor.fetchall()

            if len(rows) != 1:
                message = "No account is registered with this email"
                return render_template("login.html", message=message)
                
            # check the password hash
            if not check_password_hash(rows[0]['password_hash'], userPassword):
                message = "invalid password"
                return render_template("login.html", message=message)

            # set the user in the session
            session["user_id"] = rows[0]["id"]


        # redirect home or to history?
        return redirect("/")

    # GET method
    else:
        # render the login.html
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()

    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    # return "future home of registering a user"
    # TODO make register.html
    session.clear()
    
    # TODO write behavior for:
    # POST method
    if request.method == "POST":
        userEmail = request.form.get("email")
        userPassword = request.form.get("password")
        passwordConfirmation = request.form.get("confirm")

        # handle if the user doesn't input email or password or password confirmation
        if not userEmail or not userPassword or not passwordConfirmation:
            message = "Please enter a valid email and password and confirm your password"
            return render_template("register.html", message=message)

        # connect to the database
        con = get_db_connection()

        with con:
            con.row_factory = Row

            cursor = con.cursor()

            # check if the email is already registered
            cursor.execute("SELECT * FROM users WHERE email = ?", (userEmail,))
            checkEmailRegistration = cursor.fetchall()

            if len(checkEmailRegistration) != 0:
                # render the register.html template but with an error message?
                message = f"{checkEmailRegistration['email']} is already registered, please login or register with a different email"
                return render_template("register.html", message=message)

            # hash the password
            password_hash = generate_password_hash(userPassword)

            # insert the email and password hash into the database
            cursor.execute("INSERT INTO users (email, password_hash) VALUES (?, ?)", (userEmail, password_hash))

            con.commit()

        # redirect to login so the user can...login
        return redirect("/login")

    # GET method
    else:
        # render the register.html
        return render_template("register.html")