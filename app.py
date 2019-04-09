from flask import Flask
from flask import render_template
app = Flask(__name__)

class Header:
    def __init__(self):
        self.img = '/static/img/home-bg.jpg'
        self.title = 'Clean Blog'
        self.subTitle = 'A Blog Theme'
class Post:
    def __init__(self,title,subTitle,author,postTime):
        self.title = title
        self.subTitle = subTitle
        self.author = author
        self.postTime = postTime
class Footer:
    def __init__(self,twitter,facebook,github):
        self.twitter = twitter
        self.facebook = facebook
        self.github = github
@app.route('/')
def index():
    header = Header()
    posts = [Post('Man must explore, and this is exploration at its greatest','Problems look mighty small from 150 miles up','Start Bootstrap','September 24, 2019'),
             Post('and this is exploration at its greatest','Problems look mighty small from 150 miles up','Bootstrap','September 25, 2019')]
    footer = Footer('','','https://github.com/Emeralddddd')
    return render_template("index_r.html",title='Home',header=header,posts=posts,footer=footer)


if __name__ == '__main__':
    app.run()
