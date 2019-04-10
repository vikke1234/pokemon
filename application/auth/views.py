from flask import render_template, redirect, request, url_for
from flask_login import login_user, logout_user

from application import db, app, flask_bcrypt
from application.auth.models import User
from application.auth.forms import LoginForm, RegisterForm


@app.route("/auth/login", methods=["GET", "POST"])
def auth_login():
    if (request.method == "GET"):
        return render_template(
            "auth/loginform.html", form=LoginForm(), url="auth_login")

    form = LoginForm(request.form)

    user = User.query.filter_by(username=form.username.data).first()

    if not user or not flask_bcrypt.check_password_hash(
            user.password, form.password.data.encode("utf-8")):
        return render_template(
            "auth/loginform.html",
            form=form,
            error="Invalid username or password",
            url="auth_login")

    print("User: " + user.name + " authenticated ")
    login_user(user)
    return redirect(url_for("index"))


@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/auth/register", methods=["GET", "POST"])
def auth_register():
    if (request.method == "GET"):
        return render_template(
            "auth/loginform.html", form=RegisterForm(), url="auth_register")

    form = RegisterForm(request.form)
    user_taken = User.query.filter_by(username=form.username.data).first()
    print(user_taken)
    if user_taken:
        return render_template(
            "auth/loginform.html",
            form=RegisterForm(),
            url="auth_register",
            error="username taken")
    if not form.validate():
        return render_template(
            "auth/loginform.html",
            form=RegisterForm(),
            url="auth_register",
            error="password cannot be empty")

    pw = flask_bcrypt.generate_password_hash(
        form.password.data.encode("utf-8"))
    user = User(form.name.data, form.username.data, pw)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for("auth_login"))
