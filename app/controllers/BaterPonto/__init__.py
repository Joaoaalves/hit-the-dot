import flask
from flask import Blueprint, render_template, url_for, request, session, redirect
from app.controllers.decorators import funcionario_required, admin_required, get_user_object
from app import db, app, redis_con, mail
from datetime import datetime, timedelta

from app.models.pausa import Pausa