#! /usr/bin/env python3

from sys import version
from flask.app import Flask
from flask_wtf import FlaskForm
from sqlalchemy.sql.sqltypes import String
from wtforms import StringField, PasswordField, IntegerField, Field
from wtforms.validators import DataRequired, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    first_name = StringField('firstname', validators=[DataRequired()])
    last_name = StringField('lastname', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class LogonForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class AddBoxesForm(FlaskForm):
    hostname = StringField('hostname')
    ip_address = StringField('ip_address')
    network = StringField('network')
    object_name = StringField('object_name')


class RemoveBoxesForm(FlaskForm):
    pass


class GetBoxesForm(FlaskForm):
    filter_os = StringField('filter_os', validators=[DataRequired()])
    filter_os_cat = StringField('filter_os_cat', validators=[DataRequired()])
    filter_hostname = StringField('filter_hostname', validators=[DataRequired()])
    filter_ip = StringField('filter_ip', validators=[DataRequired()])
    page_count = IntegerField('page_count', validators=[DataRequired()])
    page_number = IntegerField('page_number', validators=[DataRequired()])


class NewNLPJobForm(FlaskForm):
    job_query = StringField('job_query', validators=[DataRequired()])


class NewJobForm(FlaskForm):
    job_item = StringField('job_item', validators=[DataRequired()]) # processes, reg keys, services
    item_name = StringField('item_name', validators=[DataRequired()]) # specificy what job_item is equal to
    os_cat = StringField('os_cat') # can be set to all or specific OS type


class ViewJobForm(FlaskForm):
    job_id = IntegerField('job_id', validators=[DataRequired()])