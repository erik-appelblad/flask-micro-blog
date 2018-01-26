from flask import Flask, render_template, request, session, make_response

from src.common.database import Database
from src.models.about import About
from src.models.blog import Blog
from src.models.post import Post
from src.models.user import User

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = "verysecret"

@app.before_first_request
def initialize_database():
    Database.initialize()

@app.route('/')
def home_template():
    return render_template('home.html')

@app.route('/login')
def login_template():
    #initialize_database()
    return render_template('login.html')

@app.route('/logout')
def logout_template():
    User.get_by_email(session['email']).logout()
    return render_template('home.html')

@app.route('/register')
def register_template():
    return render_template('register.html')

@app.route('/auth/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']

    if User.login_valid(email, password):
        User.login(email)
    else:
        session['email'] = None

    return render_template("profile.html", email=session['email'])

@app.route('/auth/register', methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']
    name = request.form['name']
    description = request.form['description']

    User.register(email, password)
    About(name, description, User.get_by_email(session['email'])._id).save_to_mongo()

    return render_template("profile.html", email=session['email'])

@app.route('/blogs/<string:user_id>')
@app.route('/blogs')
def user_blogs(user_id=None):
    if user_id is not None:
        user = User.get_by_id(user_id)
    elif session['email'] == None:
        return render_template("login.html")
    else:
        user = User.get_by_email(session['email'])

    blogs = user.get_blogs()

    return render_template("user_blogs.html", blogs=blogs, email=user.email)

@app.route('/blogs/new', methods=['POST', 'GET'])
def create_new_blog():
    if request.method == 'GET':
        return render_template("new_blog.html")
    else:
        title = request.form['title']
        description = request.form['description']
        user = User.get_by_email(session['email'])

        blog = Blog(user.email, title, description, user._id)
        blog.save_to_mongo()

        return make_response(user_blogs(user._id))  # Redirect?

@app.route('/posts/<string:blog_id>')
def blog_posts(blog_id):
    blog = Blog.from_mongo(blog_id)
    posts = blog.get_posts()
    about = About.get_by_user_id(blog.author_id)

    return render_template('posts.html', posts=posts, blog_title=blog.title, blog_id=blog_id, about=about)


@app.route('/posts/new/<string:blog_id>', methods=['POST', 'GET'])
def create_new_post(blog_id):
    if request.method == 'GET':
        return render_template('new_post.html', blog_id=blog_id)
    elif request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category = request.form['category']
        user = User.get_by_email(session['email'])

        post = Post(blog_id, title, content, category, user.email)
        post.save_to_mongo()

        return make_response(blog_posts(blog_id))  # Redirect?


if __name__ == '__main__':
    app.run(port=5555)
