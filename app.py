"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import db, connect_db, User, Post, Tag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "Phanuphanu"

connect_db(app)
db.create_all()


@app.route('/')
def home_page():
    """ Redirect to list of users """
    return redirect('/users')

@app.route('/users')
def users():
    """ Show all users """
    users = User.query.all()
    return render_template('users.html', users=users)

# Create new user
@app.route('/users/new')
def create_new_user():
    """ Show an add form for users """
    return render_template('create.html')

@app.route('/users/new', methods=['POST'])
def create_new_user_post():
    """ Process the add form, adding a new user and going back to /users """

    user = User(first_name=request.form['firstName'], last_name=request.form['lastName'], image_url=request.form['imageURL'], )

    db.session.add(user)
    db.session.commit()
    return redirect('/users')

# User Profile
@app.route('/users/<int:user_id>')
def user_profile(user_id):
    """ Show information about the given user """
    user = User.query.get_or_404(user_id)
    return render_template('profile.html', user=user)

@app.route('/users/<int:user_id>/edit')
def user_edit(user_id):
    """ Show the edit page for a user """
    user = User.query.get_or_404(user_id)
    return render_template('profile_edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def user_edit_post(user_id):
    """ Process the edit form, returning the user to the /users page """
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['firstName']
    user.last_name = request.form['lastName']
    user.image_url = request.form['imageURL']

    db.session.add(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def user_delete(user_id):
    """ Delete the user """
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')

# Posts
@app.route('/users/<int:user_id>/posts/create')
def create_post_form(user_id):
    """ Shows user interface for creating a post  """ 

    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('posts_form.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/create', methods=["POST"])
def create_post_submit(user_id):
    """ Create a new post for the user """

    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    post = Post(title=request.form['title-input'],
                    content=request.form['content-input'],
                    user_id=user_id,
                    user=user,
                    tags=tags)

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def show_post_page(post_id):
    """ Show post's content """

    post = Post.query.get_or_404(post_id)
    return render_template('posts_page.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    """ Show edit form for user's post """

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('posts_edit.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post_submit(post_id):
    """ Submit edit post form """

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title-input']
    post.content = request.form['content-input']

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post_submit(post_id):
    """ Submit delete form """

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")

#######################################################################################################################################
@app.route('/tags')
def tags_index():
    """ Show all tags """

    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)


@app.route('/tags/new')
def tags_new_form():
    """ Show tag form """

    posts = Post.query.all()
    return render_template('tags_new.html', posts=posts)


@app.route("/tags/new", methods=["POST"])
def tags_new_post():
    """ Create new tag """

    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()

    return redirect("/tags")


@app.route('/tags/<int:tag_id>')
def tags_id(tag_id):
    """ Show specific tag """

    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags_show.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit')
def tags_edit_form(tag_id):
    """ Edit a tag """

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('tags_edit.html', tag=tag, posts=posts)


@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def tags_edit_post(tag_id):
    """ Submit edit tag """

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")


@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def tags_delete(tag_id):
    """ Delete tag """
    
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect("/tags")