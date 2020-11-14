from flask import Blueprint
from flask import  render_template, request
from flaskblog.models import Post

main = Blueprint('main', __name__)

@main.route('/') # routes are what we type to go to different pages
@main.route('/home')
#@main.route is a decorator, check vids
def home():
	page = request.args.get('page', 1, type=int) #query url
	posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5, page=page)
	return render_template('home.html', posts=posts)

@main.route('/about') # create about page 
def about():
    return render_template('about.html', title='About')