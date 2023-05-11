""" 
Version 1 of Menlo student forums website
includes front and back end of
users, posting, sorting, and upvoting
created for ATCS final project

Created by: Nate Bowers
Date: 05/09/2023
"""

from flask import *
from database import init_db, db_session
from models import *
from sqlalchemy import desc
from sqlalchemy import func

app = Flask(__name__)

app.secret_key = "y5T79tFS8HhEdQxcJg=="

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method=="GET":
        session['count_users'] = db_session.query(User).count()
        return render_template('signup2.html')
    elif request.method == "POST":
        password = request.form["password"]
        username = request.form["username"]
        confirmpassword = request.form["confirm-password"]
        
        #if passwords match and if username not already taken, add user to db and log them in
        if password == confirmpassword:
            if len(db_session.query(User).where(username == User.username).all()) == 0:
                temp = User(username,password)
                db_session.add(temp)
                db_session.commit()
                session["username"]=username
                session['count_users'] = db_session.query(User).count()
                session["page"]="home"
                return redirect(url_for("home"))
            else:
                session['count_users'] = db_session.query(User).count()
                flash("username already taken", "error")
                return render_template("signup2.html")
        else:
            session['count_users'] = db_session.query(User).count()
            flash("passwords do not match", "error")
            return render_template("signup2.html")

@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method=="GET":
        session['count_users'] = db_session.query(User).count()
        return render_template("login2.html")
    elif request.method == "POST":
        #check if credentials are valid then redirect to home
        password = request.form["password"]
        username = request.form["username"]
        users = db_session.query(User).where((username == User.username) & (password ==User.password)).all()
        if len(users)==1:
            session["username"]=username
            session['count_users'] = db_session.query(User).count()
            session["page"]="home"
            return redirect(url_for('home'))
        else:
            flash("incorrect username or password", "error")
            return render_template("login2.html")


@app.route("/newpost", methods=["GET", "POST"])
def newpost():
    if "username" in session:
        if request.method=="GET":
            session['count_users'] = db_session.query(User).count()
            
            return render_template("newpost.html")
        elif request.method == "POST":
            #create and add post to database then redirect use to homepage
            topic = request.form["post-topic"]
            title = request.form["post-title"]
            content = request.form["post-content"]
            temp = Post(title,topic,content,session["username"])
            db_session.add(temp)
            db_session.commit()
            flash("Post successfully uploaded")
            session['count_users'] = db_session.query(User).count()
            session["page"]="home"
            return redirect(url_for("home"))
    else:
        flash("You need to log in")
        session['count_users'] = db_session.query(User).count()
        return redirect(url_for("login"))

@app.route("/home")
def home():
    if "username" in session:
        posts = db_session.query(Post).order_by(Post.time.desc()).all()
        session['count_users'] = db_session.query(User).count()
        session["page"]="home"
        return render_template("home.html",posts=posts)
    else:
        flash("You need to log in")
        session['count_users'] = db_session.query(User).count()
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("username")
    session['count_users'] = db_session.query(User).count()
    return redirect(url_for("login"))

#Post sorting functions
@app.route('/home/recent')
def recent():
    posts = db_session.query(Post).order_by(Post.time.desc()).all()
    session['count_users'] = db_session.query(User).count()
    session["page"]="recent"
    return render_template("home.html", posts=posts)

@app.route('/home/popular')
def popular():
    posts = db_session.query(Post).join(Upvote).group_by(Post).order_by(func.count(Upvote.post_id).desc()).all()
    session['count_users'] = db_session.query(User).count()
    session["page"]="popular"
    return render_template("home.html", posts=posts)

@app.route('/home/academics')
def academics():
    posts = db_session.query(Post).where(Post.topic =='academics').order_by(Post.time.desc()).all()
    session['count_users'] = db_session.query(User).count()
    session["page"]="academics"
    return render_template("home.html", posts=posts)

@app.route('/home/social')
def social():
    posts = db_session.query(Post).where(Post.topic =='social').order_by(Post.time.desc()).all()
    session['count_users'] = db_session.query(User).count()
    session["page"]="social"
    return render_template("home.html", posts=posts)

@app.route('/home/teachers')
def teachers():
    posts = db_session.query(Post).where(Post.topic =='teachers').order_by(Post.time.desc()).all()
    session['count_users'] = db_session.query(User).count()
    session["page"]="teachers"
    return render_template("home.html", posts=posts)

@app.route('/home/athletics')
def athletics():
    posts = db_session.query(Post).where(Post.topic =='athletics').order_by(Post.time.desc()).all()
    session['count_users'] = db_session.query(User).count()
    session["page"]="athletics"
    return render_template("home.html", posts=posts)

@app.route('/home/other')
def other():
    posts = db_session.query(Post).where(Post.topic =='other').order_by(Post.time.desc()).all()
    session['count_users'] = db_session.query(User).count()
    session["page"]="other"
    return render_template("home.html", posts=posts)

@app.route('/upvote', methods=['POST'])
def upvote():
    #save where on the page the user was for later use
    #check if user has already upvoted post
    post_id = request.form['post-id']
    anchor_input="post"+post_id
    already_exist = db_session.query(Upvote).where((Upvote.post_id == post_id) & (Upvote.upvoter_username==session["username"])).all()
    if len(already_exist)==0:
        upvote = Upvote(post_id, session["username"])
        db_session.add(upvote)
        db_session.commit()
        session['count_users'] = db_session.query(User).count()
        return redirect(url_for(session["page"], _anchor=anchor_input))
    else:
        flash("You can only upvote a post once!", "error")
        session['count_users'] = db_session.query(User).count()
        
        return redirect(url_for(session["page"],_anchor=anchor_input))

@app.before_first_request
def setup():
    init_db()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)

