#! /usr/bin/env python3

from sys import version
from flask import request
from forms import *

# from werkzeug.security import safe_str_cmp  # TODO use this
from flask_jwt_extended import create_access_token
from models import *
import bcrypt
from settings import engine
from sqlalchemy.orm import scoped_session, sessionmaker

db = scoped_session(sessionmaker(bind=engine))


def create_user():
    if request.method == "POST":
        form = RegistrationForm()
        if form.validate_on_submit():
            user = (
                db.query(Users).filter_by(username=form.username.data.lower()).first()
            )
            if user:
                return {"status": "error", "data": "username already in use"}, 400

            new_user = Users(
                pw_hash=bcrypt.hashpw(
                    (form.password.data).encode("utf-8"), bcrypt.gensalt()
                ),
                username=form.username.data.lower(),
                first_name=form.first_name.data,
                last_name=form.last_name.data,
            )
            db.add(new_user)
            db.commit()

            # confirm user commited to db
            if new_user:
                # generate user auth token
                # jwt_token = create_access_token(
                #    identity={'user_id': new_user.user_id,
                #              'username': new_user.username})

                return {"status": "success", "data": new_user.username}, 200
            else:
                return {
                    "status": "failure",
                    "data": "failed to register new user against db",
                }, 400
        else:
            return {"status": "failure", "data": form.errors}, 400
    elif request.method == "POST":
        return {}, 200


def login():
    if request.method == "POST":
        form = LogonForm()
        if form.validate_on_submit():
            user = (
                db.query(Users).filter_by(username=form.username.data.lower()).first()
            )
            if user:
                if bcrypt.checkpw(
                    (form.password.data).encode("utf-8"), user.pw_hash.encode("utf-8")
                ):
                    jwt_token = create_access_token(
                        identity={
                            "user_id": user.user_id,
                            "username": user.username.lower(),
                            "login_type": "native",
                        }
                    )
                    return {
                        "status": "success",
                        "username": user.username.lower(),
                        "data": jwt_token,
                    }, 200
                else:
                    # wrong password
                    return {
                        "status": "failure",
                        "data": "incorrect username or password",
                    }, 400
            else:
                # user does not exist, attempt LDAP login

                return {
                    "status": "failure",
                    "data": "incorrect username or password",
                }, 400
        else:
            return {"status": "error", "data": str(form.errors.items())}

    elif request.method == "OPTIONS":
        return {"status": "complete"}, 200
