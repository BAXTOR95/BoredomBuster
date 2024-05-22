from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from datetime import datetime, UTC
from . import db
from .models import User, Activity
from .forms import LoginForm, RegistrationForm, FilterForm
from .utils import fetch_random_activity

main_bp = Blueprint('main', __name__)


@main_bp.route('/', methods=['GET', 'POST'])
@main_bp.route('/index', methods=['GET', 'POST'])
def index():
    form = FilterForm()
    if form.validate_on_submit():
        try:
            result = fetch_random_activity(form.type.data, form.participants.data)
            activity = result['activity']
            if 'error' in activity:
                return jsonify({'error': activity['error']})
            image_url = result['image_url']
            return jsonify({'activity': activity, 'image_url': image_url})
        except Exception as e:
            return jsonify({'error': str(e)})
    return render_template('home.html', title='Home', form=form)


@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember_me.data)
        user.last_login = datetime.now(UTC)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('login.html', title='Sign In', form=form)


@main_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        password = form.password.data
        password2 = form.password2.data
        if password != password2:
            flash("Passwords do not match")
            return redirect(url_for("main.register"))
        user.set_password(form.password.data)
        user.last_login = None  # Set last_login to None during registration
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)


@main_bp.route('/favorites')
@login_required
def favorites():
    user = User.query.get(current_user.id)
    activities = user.activities  # Directly use the list of activities
    return render_template('favorites.html', title='Favorites', activities=activities)


@main_bp.route('/save_activity', methods=['POST'])
@login_required
def save_activity():
    data = request.json
    if not data:
        return jsonify(status='error', message='Invalid request format'), 400
    try:
        activity = Activity(
            description=data['description'],
            type=data['type'],
            participants=data['participants'],
            user_id=current_user.id,
        )
        db.session.add(activity)
        db.session.commit()
        return jsonify(status='success')
    except Exception as e:
        return jsonify(status='error', message=str(e)), 400


@main_bp.route('/remove_activity', methods=['POST'])
@login_required
def remove_activity():
    data = request.json
    activity = Activity.query.get(data['id'])
    if activity and activity.user_id == current_user.id:
        db.session.delete(activity)
        db.session.commit()
        return jsonify(status='success')
    return jsonify(status='error')
