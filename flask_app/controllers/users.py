from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.post import Post


@app.route('/')
def index():
    if 'user_id' in session:
        return redirect("/home")
    return render_template("index.html")

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect("/")
    if not Post.get_all():
        posts = False
    else:
        posts = Post.get_all()
    return render_template("home.html", userid=session['user_id'], firstname=session['first_name'], posts=posts, locs=Post.index_locations())

@app.route('/login', methods=['POST'])
def login():
    if 'user_id' in session:
        redirect("/home")
    if not User.validate_login(request.form):
        return redirect("/")
    return redirect("/home")

@app.route('/logout')
def logout():
        session.clear()
        return redirect("/")

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_registration(request.form):
        return redirect('/')
    user_id = User.register({
        "fname": request.form['fname'],
        "lname": request.form['lname'],
        "em": request.form['em'],
        "pas": request.form['pas']
    })
    session['user_id'] = user_id
    session['first_name'] = User.get_by_id({"id": user_id}).first_name
    session['last_name'] = User.get_by_id({"id": user_id}).last_name
    return redirect("/home")
