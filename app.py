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
        #db_session.query(Post).delete()
        #db_session.commit()
        count_users=db_session.query(User).count()
        return render_template('signup2.html', count_users=count_users)
    elif request.method == "POST":
        password = request.form["password"]
        username = request.form["username"]
        confirmpassword = request.form["confirm-password"]
        key = request.form["secretkey"]
        
        #if passwords match and if username not already taken, add user to db and log them in
        if password == confirmpassword:
            
            if len(db_session.query(User).where(username == User.username).all()) == 0:
             
                temp = User(username,password)
                db_session.add(temp)
                db_session.commit()
                session["username"]=username
                count_users=db_session.query(User).count()
                logged_in_user=db_session.query(User).where(User.username == session["username"]).first()
                return redirect(url_for("home", u=logged_in_user,count_users=count_users))
            else:
                count_users=db_session.query(User).count()
                flash("username already taken", "error")
                return render_template("signup2.html", count_users=count_users)
        else:
            count_users=db_session.query(User).count()
            flash("passwords do not match", "error")
            return render_template("signup2.html", count_users=count_users)

@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method=="GET":
        count_users=db_session.query(User).count()
        return render_template("login2.html", count_users=count_users)
    elif request.method == "POST":
        #check if credentials are valid
        password = request.form["password"]
        username = request.form["username"]
        users = db_session.query(User).where((username == User.username) & (password ==User.password)).all()
        if len(users)==1:
            session["username"]=username
            count_users=db_session.query(User).count()
            logged_in_user=db_session.query(User).where(User.username == session["username"]).first()
            return redirect(url_for('home', count_users=count_users, u=logged_in_user))
        else:
            flash("incorrect username or password", "error")
            return render_template("login2.html", count_users=count_users)


@app.route("/newpost", methods=["GET", "POST"])
def newpost():
    if "username" in session:
        if request.method=="GET":
            count_users=db_session.query(User).count()
            logged_in_user=db_session.query(User).where(User.username == session["username"]).first()
            return render_template("newpost.html", count_users=count_users,u=logged_in_user)
        elif request.method == "POST":
            topic = request.form["post-topic"]
            title = request.form["post-title"]
            content = request.form["post-content"]
            temp = Post(title,topic,content,session["username"])
            db_session.add(temp)
            db_session.commit()
            flash("Post successfully uploaded")
            count_users=db_session.query(User).count()
            logged_in_user=db_session.query(User).where(User.username == session["username"]).first()
            return redirect(url_for("home", count_users=count_users, u=logged_in_user))
    else:
        flash("You need to log in")
        count_users=db_session.query(User).count()
        return redirect(url_for("login", count_users=count_users))

@app.route("/home")
def home():
    if "username" in session:
        posts = db_session.query(Post).order_by(Post.time.desc()).all()
        count_users=db_session.query(User).count()
        logged_in_user=db_session.query(User).where(User.username == session["username"]).first()
        return render_template("home.html",posts=posts, count_users=count_users, u=logged_in_user)
    else:
        flash("You need to log in")
        count_users=db_session.query(User).count()
        return redirect(url_for("login", count_users=count_users))

@app.route("/logout")
def logout():
    session.pop("username")
    count_users=db_session.query(User).count()
    return redirect(url_for("login", count_users=count_users))

@app.route('/home/recent')
def recent():
    posts = db_session.query(Post).order_by(Post.time.desc()).all()
    count_users=db_session.query(User).count()
    logged_in_user=db_session.query(User).where(User.username == session["username"]).first()
    return render_template("home.html", posts=posts, count_users=count_users, u=logged_in_user)

@app.route('/home/popular')
def popular():
    posts = db_session.query(Post).join(Upvote).group_by(Post).order_by(func.count(Upvote.post_id).desc()).all()
    count_users=db_session.query(User).count()
    logged_in_user=db_session.query(User).where(User.username == session["username"]).first()
    return render_template("home.html", count_users=count_users, posts=posts, u=logged_in_user)

@app.route('/home/academics')
def academics():
    posts = db_session.query(Post).where(Post.topic =='academics').order_by(Post.time.desc()).all()
    count_users=db_session.query(User).count()
    logged_in_user=db_session.query(User).where(User.username == session["username"]).first()
    return render_template("home.html", count_users=count_users, posts=posts, u=logged_in_user)

@app.route('/home/social')
def social():
    posts = db_session.query(Post).where(Post.topic =='social').order_by(Post.time.desc()).all()
    count_users=db_session.query(User).count()
    logged_in_user=db_session.query(User).where(User.username == session["username"]).first()
    return render_template("home.html", count_users=count_users, posts=posts, u=logged_in_user)

@app.route('/home/teachers')
def teachers():
    posts = db_session.query(Post).where(Post.topic =='teachers').order_by(Post.time.desc()).all()
    count_users=db_session.query(User).count()
    logged_in_user=db_session.query(User).where(User.username == session["username"]).first()
    return render_template("home.html", count_users=count_users, posts=posts, u=logged_in_user)

@app.route('/home/athletics')
def athletics():
    posts = db_session.query(Post).where(Post.topic =='athletics').order_by(Post.time.desc()).all()
    count_users=db_session.query(User).count()
    logged_in_user=db_session.query(User).where(User.username == session["username"]).first()
    return render_template("home.html", count_users=count_users, posts=posts, u=logged_in_user)

@app.route('/home/other')
def other():
    posts = db_session.query(Post).where(Post.topic =='other').order_by(Post.time.desc()).all()
    count_users=db_session.query(User).count()
    logged_in_user=db_session.query(User).where(User.username == session["username"]).first()
    return render_template("home.html", count_users=count_users, posts=posts, u=logged_in_user)

@app.route('/upvote', methods=['POST'])
def upvote():
    post_id = request.form['post-id']
    anchor_input="post"+post_id
    already_exist = db_session.query(Upvote).where((Upvote.post_id == post_id) & (Upvote.upvoter_username==session["username"])).all()

    if len(already_exist)==0:
        upvote = Upvote(post_id, session["username"])
        db_session.add(upvote)
        db_session.commit()
        count_users=db_session.query(User).count()
        logged_in_user=db_session.query(User).where(User.username == session["username"]).first()
        return redirect(url_for('home', count_users=count_users, u=logged_in_user, _anchor=anchor_input))
    else:
        flash("You can only upvote a post once!", "error")
        count_users=db_session.query(User).count()
        logged_in_user=db_session.query(User).where(User.username == session["username"]).first()
        return redirect(url_for("home", count_users=count_users, u=logged_in_user,_anchor=anchor_input))

@app.before_first_request
def setup():
    init_db()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)

