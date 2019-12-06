#NEVEN MARIC
#Concordia University
#ID: 40031001
#SOEN 287

import csv

from flask import Flask, url_for, render_template, request, flash, session, redirect
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user


app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.config['SECRET_KEY'] = "lkkajdghdadkglajkgah"

#LOGGED = "Login" #used to specify in top right corner whether user needs to login


class User(UserMixin):
  def __init__(self,id):
    self.id = id

def is_user_logged():
    """Checks if user is logged and adjusts pages accordingly"""
    try:
        if session["username"] is not None and session["username"] in ["Neven", "Tiffany"]:
            print("WOWOWOWOWOWOWOWWO")
            print(session["username"])
            return "Logout"
        else:
            return "Login"
    except:
        return "Login"

@login_manager.user_loader
def load_user(user_id):
    """Loads users"""
    return User(user_id)

@app.route('/logmein')
def logmein():
    """Goes to login page or logs out."""
    try:
        if session["username"] in ["Neven", "Tiffany"]:
            print("LOGGING OUT SON")
            logout_user()
            session.pop('username', None)
            print(session["username"])
    except:
        pass
    return render_template("login.html", logged=is_user_logged())

@app.route('/login', methods=['POST'])
def login():
    """Handles logging in."""
    if check_password(request.form["username"], request.form["password"]):
        login_user(User(request.form["username"]))
        session["username"] = request.form["username"]
        return render_template("index.html", logged=is_user_logged())
    else:
        session["username"] = None
        return render_template("login.html", logged=is_user_logged(), wrong_login="Username and/or Password Incorrect")

def check_password(username, password):
    """Checks password to see if valid"""
    username1 = "Neven"
    username2 = "Tiffany"
    password1 = "Tiffany12"
    password2 = "Nevenisthebest"
    if username == username1 and password == password1:
        return True
    elif username == username2 and password == password2:
        return True
    else:
        return False

@app.route('/protected')
def protected():
    """Protected page that can only be seen if user is logged in."""
    if current_user.is_authenticated:
        return render_template('correct_information.html', logged=is_user_logged())
    else:
        return render_template('login.html', logged=is_user_logged())

@app.route('/')
def index():
    """Main page."""
    return render_template("index.html", logged=is_user_logged())

@app.route('/contact')
def contact():
    """Contact me page."""
    return render_template("contact.html", logged=is_user_logged())

@app.route('/contact_form', methods=['POST'])
def handle_contact_form():
    """Handles user applications."""
    with open('data/messages.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([request.form['name'], 
                         request.form['email'], 
                         request.form['phone'],
                         request.form['position'],
                         request.form['experience'],
                         request.form['about_you']])
    return render_template('contact_response.html', 
                           data=request.form, logged=is_user_logged())

@app.route('/contact_neven_form', methods=['POST'])
def handle_contact_neven_form():
    """Handles contact me form to decide if user is allowed to contact me."""
    if request.form['enjoy'].lower() == "yes" and \
        request.form['pizza'].lower() == "yes" and \
        request.form['bestage'] == '25' and \
        request.form['sport'].lower() == "boxing" and \
        request.form['king'].lower() == "neven" and \
        request.form['messi'].lower() == 'messi' and \
        request.form['jordan'].lower() == "jordan" and \
        request.form['justin'].lower() == "below" and \
        request.form['concordia'].lower() == "concordia" and \
        request.form['mayweather'].lower() == "mayweather":
        return render_template('correct_information.html', logged=is_user_logged())
    else:
        return render_template('sorry.html', logged=is_user_logged())

@app.route('/mainbase')
def mainbase():
    """Shows main base page."""
    return render_template("mainbase.html", logged=is_user_logged())

@app.route('/upcoming')
def upcoming():
    """Shows upcoming page."""
    return render_template("upcoming.html", logged=is_user_logged())

@app.route('/world_map')
def world_map():
    """Shows world map page."""
    images = ["static/pictures/world_map.JPG", "static/pictures/mainbase/base_map.jpeg"]
    return render_template("world_map.html", images=images, logged=is_user_logged())

@app.route('/about')
def about():
    """Shows about page."""
    return render_template("about.html", logged=is_user_logged())

@app.route('/opportunities')
def opportunities():
    """Shows opportunities page."""
    return render_template("opportunities.html", logged=is_user_logged())

@app.route('/contraptions')
def contraptions():
    """Shows contraptions page."""
    pictures = []
    titles = []
    descriptions = []
    with open('data/contraptions_list.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                continue
            pictures.append(row[0])
            titles.append(row[1])
            descriptions.append(row[2])
    table_list = []
    with open('data/contraptions_table.csv') as csv_file2:
        csv_reader2 = csv.reader(csv_file2, delimiter=',')
        line_count = 0
        for row in csv_reader2:
            if line_count == 0:
                line_count += 1
                continue
            table_list.append(row)
    # import pdb; pdb.set_trace()
    slide_list = zip(pictures, titles, descriptions)
    return render_template(
        "contraptions.html", 
        slide_list=slide_list,
        table_list=table_list,
        logged=is_user_logged())

if __name__ == '__main__':
    app.run(threaded=True, port=5000)
