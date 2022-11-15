# Mood Tracker

### Video Demo: url will go here

### Description:
Hello, I'm Pete Hamrick. The goal with Mood Tracker was to create an app that would allow a user to rate their current mood and pair that with the current weather conditions. Over time this would allow the user to draw some conclusions about their mood as it relates to the weather. For the weather data I decided to use OpenWeather. I thought seeing the data in chart form could also be useful to the user and so I used Highcharts to build build a line graph charting the users mood data.

App.py is the backbone of the app. This is where Flask is being run and where all of the route handling happens. I use `dotenv` so that I can use my API key and also send code up to github without exposing that API key to bad actors. I'll discuss what individual routes do when I go over the template files. But, broadly speaking the things happning in app.py in addition to rendering the html include: inserting and getting user data from the database, making API calls to the OpenWeather API, error handling incorrect user input for their email and password, and formatting data to pass to the HTML and ultimately render the Highcharts graph.

The schema.sql file was created to be the schema of the database containing 3 tables(users, journals, and weather). The users table simply stores the users login information. The journals table stores the mood rating and supplemental text (journal text, if you will) to provide some context for the users mood rating. Finally, the weather table stores the current weather at the time of the journal entry. The db.py file was a simple way for me to create a database using the schema file.

The helpers.py file contains 2 functions that get used in app.py but I just thought they cluttered up app.py so I moved them into a helper file and import them into the main app file. The `get_db_connection()` function lets me quickly connect to the database in order to get or add data. the `getWeather()` function calls the weather API and returns the current weather based on the users location.

Now for the templates directory in the project. This houses all the html files that the app will render.
- Layout.html is the html template that all the other html files are built on, it conditionally renders different navbar contents depending on if the user is logged in or not.
- Register and login are simple forms that take in user input for an email and password, check the database, and resolve or display a message depending on if the user succeeded or failed to properly fill them out. 
- Index.html will conditionally render a welcome that changes slightly if the user is logged in or not.
- Location.html utilizes some javascript to get the users current location and fills in some inputs on a form. It also allows the user to pick their preferred temperature units. I set the default to fahrenheit because that is what I use and also the default for OpenWeather is Kelvin which I doubt most people use. This is all inside a form and so when the user submits the form it redirects to "/log".
- Log.html on load fetches the current weather based on the users location and then renders that weather to the page. Additionally, it asks the user to rate their mood and provide some additional context. On submission of this form it will write the mood and weather to their respective tables in the database and then redirect to the users history.
- History.html fetches all of the users moods from the database and renders them on the screen in the form of a table.
- Trends.html renders the Highcharts line graph to the screen to show the users mood overtime.