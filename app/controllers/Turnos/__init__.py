from app import app, db
import flask
from flask import Blueprint, render_template, url_for, redirect, session, request

from app.models.turno import Turno
from app.models.funcionario import Funcionario

from app.controllers.decorators import admin_required, get_user_object, is_admin, funcionario_required

from datetime import datetime, timedelta
from workalendar.america.brazil import BrazilDistritoFederal
from dateutil.rrule import rrule, DAILY