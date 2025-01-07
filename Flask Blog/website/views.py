from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import login_required, current_user
from .models import Post, User, Comment
from . import db

views = Blueprint("views", __name__)

@views.route("/")
@login_required
def home():
    posts = Post.query.all()
    return render_template("home.html", user=current_user, posts=posts, cuser=current_user)

@views.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method=='POST':
        text = request.form.get('text')

        if not text:
            flash('Post should contain something.', category="error")

        else:
            new_post = Post(text=text, author=current_user.id)
            db.session.add(new_post)
            db.session.commit()
            flash('Post created.', category="success")
            return redirect(url_for('views.home'))


    return render_template("create_post.html", user=current_user, cuser=current_user)


@views.route('/delete-post/<id>')
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    
    if not post:
        flash('Post does not exist.', category="error")

    elif current_user.id != post.author:
        flash('You do not have permission to delete this post.', category="error")

    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted successfully.', category="success")
        
        
    return redirect(url_for('views.home'))    


@views.route('/user/<username>')
@login_required
def user_post(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('User does not exists.', category='success')
        return redirect(url_for('views.home'))

    posts = user.posts

    return render_template("home.html", user=username, posts=posts, cuser=current_user)

@views.route('/create-comment/<post_id>', methods=['GET', 'POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('text')
    print(text)

    if not text:
        flash('Comment cannot be empty', category='error')

    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
            flash('Comment Added.', category='success')

        else:
            flash('Post does not exist.', category='error')

    return redirect(url_for('views.home'))

@views.route('/delete-comment/<comment_id>')
def delete(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()
    
    if not comment:
        flash('Comment does not exist.', category="error")

    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('You do not have permission to delete this comment.', category="error")

    else:
        db.session.delete(comment)
        db.session.commit()
        flash('Comment deleted successfully.', category="success")
        
        
    return redirect(url_for('views.home'))    