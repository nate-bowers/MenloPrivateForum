from flask import *
from database import init_db, db_session
from models import *

app = Flask(__name__)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method=="GET":
        return render_template('signup2.html')
    elif request.method == "POST":
        password = request.form["password"]
        username = request.form["username"]
        confirmpassword = request.form["confirm-password"]
        if password == confirmpassword:
            if username not in db_session.query(User.username).where(username == User.username).all():
            #figure out how to check if user exists
                temp = User(username,password)
                db_session.add(temp)
                db_session.commit()
                session["username"]=username
                return redirect(url_for("home"))
            else:
                flash("passwords do not match", "error")
        else:
            flash("username already taken", "error")

@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method=="GET":
        return render_template("login2.html")
    elif request.method == "POST":
        #check if credentials are valid
        password = request.form["password"]
        username = request.form["username"]
        users = db_session.query(User.username).where((username == User.username) & (password ==User.password)).all()
        if len(users)==1:
            session["username"]=username
            return redirect(url_for("home"))
        else:
            flash("incorrect username or password", "error")


@app.route("/newpost", methods=["GET", "POST"])
def newpost():
    if request.method=="GET":
        return render_template("newpost.html")
    elif request.method == "POST":
        topic = request.form["post-topic"]
        title = request.form["post-title"]
        content = request.form["post-content"]
        temp = Post(title,topic,content,session["username"])
        db_session.add(temp)
        db_session.commit()
        flash("Post successfully uploaded")
        return redirect(url_for("home"))

@app.route("/home")
def home():
    return render_template("home.html")

@app.before_first_request
def setup():
    init_db()

if __name__ == "__main__":
    app.run(debug=True)

