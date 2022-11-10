from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "hello, welcome to the home page"
    # TODO make index.html
    # return render_template("index.html")

@app.route("/login")
def login():
    return "future home of logging in for registered users"
    # TODO make login.html
    # TODO write behavior for:
        # POST method
            # handle if the user doesn't input an email or password
            # connect to the database
            # find user in the database by their email
                # check the password hash
            # set the user in the session
            # redirect home or to history?
        # GET method
            # render the login.html


@app.route("/register")
def register():
    return "future home of registering a user"
    # TODO make register.html
    # TODO write behavior for:
        # POST method
            # handle if the user doesn't input email or password or password confirmation
            # connect to the database
            # check if the email is already registered
                # render the register.html template but with an error message?
            # hash the password
            # insert the email and password hash into the database
            # redirect to login so the user can...login
        # GET method
            # render the register.html