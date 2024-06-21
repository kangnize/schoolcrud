from flask import render_template, url_for, flash, redirect, Blueprint, request
from app import db, bcrypt
from app.forms import RegistrationForm, LoginForm, EditForm
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required
import os
import secrets
from flask import current_app
from PIL import Image

bp = Blueprint('main', __name__)

@bp.route("/")
@bp.route("/home")
def home():
    return render_template('home.html')

@bp.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.base'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)

@bp.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.base'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('You have been logged in successfully.', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.account'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('main.home'))

@bp.route("/account")
@login_required
def account():
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', user=current_user, image_file=image_file)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@bp.route("/account/edit", methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm()
    if form.validate_on_submit():
        if form.email.data != current_user.email:
            user_with_same_email = User.query.filter_by(email=form.email.data).first()
            if user_with_same_email and user_with_same_email.id != current_user.id:
                flash('This email is already in use. Please choose a different one.', 'danger')
                return redirect(url_for('main.edit'))

        if form.username.data != current_user.username:
            user_with_same_username = User.query.filter_by(username=form.username.data).first()
            if user_with_same_username and user_with_same_username.id != current_user.id:
                flash('This username is already in use. Please choose a different one.', 'danger')
                return redirect(url_for('main.edit'))

        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.password.data:
            current_user.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('main.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('edit.html', title='Edit Account', form=form)

@bp.route("/account/delete", methods=['GET', 'POST'])
@login_required
def delete_account():
    if request.method == 'POST':
        user_id = current_user.id
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        logout_user()
        flash('Your account has been deleted.', 'success')
        return redirect(url_for('main.home'))
    return render_template('delete_account.html', title='Delete Account')
