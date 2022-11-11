from flask import Flask, render_template, request, session, redirect
from flask_session import Session
from sqlite3 import Error, connect

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
        
        return redirect("/")
            # connect to the database
            # find user in the database by their email
                # check the password hash
            # set the user in the session
            # redirect home or to history?
        # GET method
            # render the login.html


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
        # check if the email is already registered
            # render the register.html template but with an error message?
        # hash the password
        # insert the email and password hash into the database
        # redirect to login so the user can...login

    # GET method
    else:
        # render the register.html
        return render_template("register.html")