from flask import render_template, flash, redirect, request,url_for
from app import app
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import current_user,login_user,logout_user,login_required
from app.models import User,db,Post,PostForm,Footer,Header

header1 = Header('/static/img/home-bg.jpg', 'Title', 'Love U')
@app.route('/index')
@app.route('/')
def index():
    if current_user.is_anonymous:
        username='Guest'
    else:
        username=current_user.username
    header = Header('/static/img/home-bg.jpg',username,'Love U')
    if current_user.is_anonymous:
        posts = None
    else:
        posts = current_user.my_posts().paginate(1,2,False).items
    return render_template("index_r.html", title='Home', header=header, posts=posts)
    #return "Hello World!"

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('Username')).first()
        passwd = request.form.get('Password')
        if user is None or not user.check_password(passwd):
            flash('Invalid username or password','error')
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
    pid = request.args.get('id',1,type=int)
    p=Post.query.filter_by(id=pid).first()
    return render_template('post_r.html',title='test',header=Header('/static/img/post-bg.jpg','username','Love U'),body=p.body)

@login_required
@app.route('/newpost',methods=['POST','GET'])
def newpost():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
    return render_template('newpost.html',title='new',form=form)

@app.route('/postlist')
def postlist():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('postlist', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('postlist', page=posts.prev_num) \
        if posts.has_prev else None

    return render_template('postlist.html',title='postlist',header=header1,posts=posts.items,next_url=next_url,prev_url=prev_url)