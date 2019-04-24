from flask import render_template, flash, redirect, request, url_for
from app import app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, db, Post, PostForm, Footer, Header, PostForm1,Tag

header1 = Header('https://source.unsplash.com/random/400*300', 'Guest', 'Love U')


# def login_jump(func):
#     def wrapper():
#         if current_user.is_anonymous:
#             flash("请登陆以继续")
#             return redirect('/login')
#         else:
#             func()
#     return wrapper()

@app.route('/index')
@app.route('/')
def index():
    if current_user.is_anonymous:
        posts = None
    else:
        posts = current_user.my_posts().paginate(1, 2, False).items
        header1.title = current_user.username
    return render_template("index_r.html", title='Home', header=header1, posts=posts)
    # return "Hello World!"
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('Username')).first()
        if user:
            return redirect('/')
        else:
            user = User(username=request.form.get('Username'),password_hash=generate_password_hash(request.form.get('Password')))
            db.session.add(user)
            db.session.commit()
        return redirect('/login')
    return render_template('register.html',title='Register')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('Username')).first()
        passwd = request.form.get('Password')
        if user is None or not user.check_password(passwd):
            flash('Invalid username or password', 'error')
            return redirect('login')
        login_user(user)
        return redirect('login')
    return render_template('login.html', title='Login in', header=None)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/post')
def post():
    pid = request.args.get('page', 1, type=int)
    p = Post.query.filter_by(id=pid).first()
    return render_template('post_r.html', title='test', header=header1, post=p)


@app.route('/newpost', methods=['POST', 'GET'])
@login_required
def newpost():
    # post = Post(body=form.body.data, title=form.title.data,abs=form.abs.data, author=current_user)
    # db.session.add(post)
    # db.session.commit()
    # flash('Your post is now live!')

    if request.method == 'POST':
        post = Post(title=request.form.get("Title"), body=request.form.get('ckeditor'),
                    user_id=current_user.id)
        abs = request.form.get('subTitle')
        print(abs)
        tags = abs.split()
        for name in tags:
            print(name)
            tag = Tag.query.filter_by(name=name).first()
            if not tag:
                tag = Tag(name=name)
                db.session.add(tag)
            post.tags.append(tag)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect('/')
    return render_template('newpost.html', title='new', header=header1)


@app.route('/postlist')
def postlist():
    page = request.args.get('page', 1, type=int)
    userid = request.args.get('user', 0, type=int)
    tagname = request.args.get('tag',type=str)
    if userid:
        posts = Post.query.filter(Post.user_id == userid).order_by(Post.timestamp.desc()).paginate(
            page, app.config['POSTS_PER_PAGE'], False)
    if tagname:
        tag = Tag.query.filter_by(name=tagname).first()
        posts = tag.post.paginate(
            page, app.config['POSTS_PER_PAGE'], False)
    else:
        posts = Post.query.order_by(Post.timestamp.desc()).paginate(
            page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('postlist', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('postlist', page=posts.prev_num) \
        if posts.has_prev else None

    return render_template('postlist.html', title='postlist', header=header1, posts=posts.items, next_url=next_url,
                           prev_url=prev_url, pager=posts,User=User)


@app.route('/myhome')
def myhome():
    return render_template('myhome.html')


@app.route('/mypost')
def mypost():
    page = request.args.get('page', 1, type=int)
    posts = current_user.my_posts().paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('postlist', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('postlist', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('postlist.html', title='postlist', header=header1, posts=posts.items, next_url=next_url,
                           prev_url=prev_url, pager=posts)

@app.route('/user')
def user():
    uid = request.args.get('id',0,type=int)
    if current_user.id==uid or uid==0:
        return redirect('/myhome')

@app.route('/profile')
def profile():
    uid = request.args.get('id', 0, type=int)
    if uid==0:
        uid = current_user.id
    u = User.query.filter_by(id=uid).first()
    return render_template('profile.html',title='profile',u=u)

@app.route('/ball')
def ball():
    return render_template('ball.html')

