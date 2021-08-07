from flask import render_template, request, redirect, url_for
from .import bp as auth
from .forms import LoginForm, RegisterForm
from .models import User
from flask_login import login_user, logout_user, current_user, login_required

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            new_user_data = {
                'first_name' : form.first_name.data.title(),
                'last_name' : form.last_name.data.title(),
                'email' : form.email.data.lower(),
                'password' : form.password.data
            }
            new_user_object = User()
            new_user_object.from_dict(new_user_data)
        except:
            error_string = "There was a problem creating your account, please try again"
            return render_template('register.html.j2', form=form, error = error_string)
        return redirect(url_for('auth.login'))
    return render_template('register.html.j2', form=form)


# used to display the login page - all the routes below
@auth.route('/', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        print('Here')
        print(password)
        user_account = User.query.filter_by(email=email).first()
        print(user_account)
        if user_account is not None and user_account.check_hashed_password(password):
            login_user(user_account)
            return redirect(url_for('main.pokemon'))
        else:
            return redirect(url_for('auth.login'))

        # if email in app.config.get('REGISTERED_USERS', {}).keys() and\
        #      password == app.config.get('REGISTERED_USERS', {}).get(email).get('password'):
        #      return f"Login was successful, Welcome {app.config.get('REGISTERED_USERS', {}).get(email).get('name')}"
        # error_string = "Incorrect Email/Password"
        # return render_template("index.html.j2", form=form, error=error_string)
    return render_template("index.html.j2", form=form)
        


@auth.route('/logout', methods=['GET', 'POST'])
@login_required        
def logout():
    if current_user:
        logout_user()
        return redirect(url_for('auth.login'))