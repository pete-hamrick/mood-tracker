from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session
from sqlite3 import Row
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from helpers import get_db_connection, getWeather

load_dotenv()
 
app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/history")
def history():
    con = get_db_connection()

    with con:
        con.row_factory = Row

        cur = con.cursor()

        cur.execute("""
            SELECT journals.date, journals.body, journals.mood, weather.title, weather.icon, weather.temp FROM journals
            INNER JOIN weather ON journals.id = weather.journal_id
            WHERE journals.user_id = ?;
        """, (session["user_id"],))

        rows = cur.fetchall()
            
    return render_template("history.html", rows=rows)

@app.route("/location", methods=["GET", "POST"])
def location():

    if request.method == "POST":

        units = request.form.get("units")
        lat = request.form.get("lat")
        lon = request.form.get("lon")
        return redirect(url_for('log', units=units, lat=lat, lon=lon))

    else:
        return render_template("location.html")

@app.route("/log", methods=["GET", "POST"])
def log():

    if request.method == "POST":
        
        title = request.form.get("title"),
        description = request.form.get("description"),
        icon = request.form.get("icon"),
        temp = request.form.get("temp"),
        feels_like = request.form.get("feels_like"),
        cloudiness = request.form.get("cloudiness")

        mood_rating = request.form.get("mood_rating"),
        mood_body = request.form.get("mood_body"),
        user_id = session['user_id']

        con = get_db_connection()

        with con:
            con.row_factory = Row

            cur = con.cursor()

            cur.execute("INSERT INTO journals (body, mood, user_id) VALUES (?, ?, ?) RETURNING *", (mood_body[0], int(mood_rating[0]), int(user_id)))

            journalRows = cur.fetchall()
            journal_id = journalRows[0]['id']

            print(journal_id)

            cur.execute("INSERT INTO weather (title, description, icon, temp, feels_like, cloudiness, journal_id) VALUES (?, ?, ?, ?, ?, ?, ?)", (title[0], description[0], icon[0], float(temp[0]), float(feels_like[0]), str(cloudiness), int(journal_id)))

            con.commit()
        return redirect("/history")

    else:
        units=request.args.get("units") 
        lat=request.args.get("lat")
        lon=request.args.get("lon")
        data = getWeather(units, lat, lon)
            
        return render_template(
            "log.html", 
            title=data["title"],
            description=data["description"], 
            temp=data["temp"], 
            feels_like=data["feels_like"], 
            cloudiness=data["cloudiness"], 
            icon=data["icon"]
        )

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