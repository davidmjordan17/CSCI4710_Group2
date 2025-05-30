from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

# Routes for the authentication blueprint
# This blueprint handles the authentication-related routes (URLS)

# Login route
# This route handles the login functionality
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect password, try again.", category='error')
        else:
            flash("Email does not exist.", category='error')
    return render_template('login.html', user=current_user)

# Logout route
# This route handles the logout functionality
# When the user clicks the logout button, they are logged out and redirected to the login page
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


# Sign-up route
# This route handles the sign-up functionality
# When the user clicks the sign-up button, they are redirected to the sign-up page
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        password = request.form.get('password')
        confirmPassword = request.form.get('confirmPassword')

        user = User.query.filter_by(email=email).first()

        if user:
            flash("Email already exists.", category='error')
        elif len(email) < 4:
            flash("Email must be greater than 4 characters.", category='error')
        elif len(firstName) < 2:
            flash("First name must be greater than 2 characters.", category='error')
        elif password != confirmPassword:
            flash("Passwords don't match.", category='error')
        elif len(password) < 7:
            flash("Password must be at least 7 characters.", category='error')
        else:
            flash("Account created!", category='success')
            
            # Create new user
            new_user = User(email=email, first_name=firstName, last_name=lastName, password=generate_password_hash(password, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        
    return render_template('signup.html', user=current_user)