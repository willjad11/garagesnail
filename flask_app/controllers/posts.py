from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.post import Post
from flask_app.models.user import User
from datetime import datetime

@app.route('/new')
def new_post():
    if 'user_id' not in session:
        return redirect("/")
    return render_template("add_posting.html", userid=session['user_id'], firstname=session['first_name'], date=datetime.now().date(), locs=Post.index_locations())

@app.route('/new/create', methods=['POST'])
def create_post():
    if 'user_id' not in session:
        return redirect("/")
    if not Post.validate_post(request.form):
        return redirect('/new')
    id = Post.create_new({
        "ptitle": request.form['ptitle'],
        "pdesc": request.form['pdesc'],
        "padd": request.form['padd'],
        "pcity": Post.extract_city(request.form['padd']),
        "pstate": Post.extract_state(request.form['padd']),
        "plid": request.form['plid'],
        "pdate": request.form['pdate'],
        "ptime": request.form['ptime'],
        "uid": session['user_id']
    })
    return redirect("/post/" + str(id))

@app.route('/post/<int:id>')
def show_post(id):
    if 'user_id' not in session:
        return redirect("/")
    post = Post.get_post_by_id({"id": id})
    gStart = Post.datetimeconvert(post.saledate, post.saletime)
    return render_template("show_posting.html", post=post, firstname=session['first_name'], gStart=gStart, locs=Post.index_locations())

@app.route('/edit/<int:id>')
def edit_post(id):
    if 'user_id' not in session:
        return redirect("/")
    post = Post.get_post_by_id({"id": id})
    if int(session['user_id']) != int(post.user_id):
        return redirect("/home")
    return render_template("edit_posting.html", userid=session['user_id'], firstname=session['first_name'], post=post, locs=Post.index_locations())

@app.route('/edit/<int:id>/confirm', methods=['POST'])
def confirm_edit_post(id):
    post = Post.get_post_by_id({"id": id})
    if 'user_id' not in session:
        return redirect("/")
    if not Post.validate_post(request.form):
        return redirect('/edit/' + str(id))
    if int(session['user_id']) != int(post.user_id):
        return redirect("/home")
    Post.edit({
        "ptitle": request.form['ptitle'],
        "pdesc": request.form['pdesc'],
        "padd": request.form['padd'],
        "pcity": Post.extract_city(request.form['padd']),
        "pstate": Post.extract_state(request.form['padd']),
        "plid": request.form['plid'],
        "pdate": request.form['pdate'],
        "ptime": request.form['ptime'],
        "pid": id
    })
    return redirect('/post/' + str(id))

@app.route('/delete/<int:id>')
def delete_post(id):
    if 'user_id' not in session:
        return redirect("/")
    post = Post.get_post_by_id({"id": id})
    if int(session['user_id']) != int(post.user_id):
        return redirect("/home")
    Post.delete({"pid": id})
    return redirect('/myposts')

@app.route('/myposts')
def my_posts():
    if 'user_id' not in session:
        return redirect("/")
    posts = User.get_posts({"uid": int(session['user_id'])})
    return render_template("my_postings.html", posts=posts, firstname=session['first_name'], locs=Post.index_locations())

@app.route('/search/<string:search>')
def search_posts(search):
    if 'user_id' not in session:
        return redirect("/")
    posts = Post.search(search)
    return render_template("search_posts.html", firstname=session['first_name'], locs=Post.index_locations(), posts=posts, search=search)
