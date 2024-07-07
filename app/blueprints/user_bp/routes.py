from flask import render_template, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from . import user_bp
from .forms import RegistrationForm, LoginForm, ForgotPasswordForm, ResetPasswordForm
from ...models.models import User, db
from ... import login_manager, mail
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.user_email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            return redirect(url_for('user_bp.dashboard'))

        flash('WRONG DATA', 'danger')
    return render_template('login.html', form=form)


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, user_email=form.user_email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Reg ok', 'success')
        return redirect(url_for('user_bp.login'))

    return render_template('register.html', form=form)


@user_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.index'))

    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.user_email.data).first()
        if user:
            send_password_reset_email(user)
            flash('Check your email', 'success')
            return redirect(url_for('user_bp.login'))

        flash('WRONG DATA', 'danger')
    return render_template('forgot_password.html', form=form)


@user_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.index'))

    user = verify_reset_token(token)
    if not user:
        return redirect(url_for('main_bp.index'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset', 'success')
        return redirect(url_for('user_bp.login'))

    return render_template('new_password.html', form=form)


def send_password_reset_email(user):
    token = generate_reset_token(user)
    msg = Message('Reset Your Password', recipients=[user.user_email])
    msg.body = f'''To reset your password, visit the following link: 
                    {url_for('user_bp.reset_password', token=token, _external=True)}
                    If you did not make this request, simply ignore this email and no changes will be made.
                '''
    mail.send(msg)


def generate_reset_token(user, expires_sec=1800):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return s.dumps(user.id, salt='password-reset-salt')


def verify_reset_token(token, expires_sec=1800):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        user_id = s.loads(token, salt='password-reset-salt', max_age=expires_sec)

    except:
        return None
    return User.query.get(user_id)


@user_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main_bp.index'))
