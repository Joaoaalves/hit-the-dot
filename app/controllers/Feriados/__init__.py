from app import app, db
import flask
from flask import render_template, url_for, request, session, redirect, Blueprint, abort

from app.controllers.decorators import funcionario_required, admin_required ,get_user_object

from datetime import datetime