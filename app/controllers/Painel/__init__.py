import flask
from flask import Blueprint, render_template, redirect, url_for, session, request

from app import db, app

from app.controllers.decorators import admin_required, funcionario_required, get_user_object, is_admin, is_admin, is_func

from datetime import datetime, timedelta, date

from time import strptime
from workalendar.america.brazil import BrazilDistritoFederal
from dateutil.rrule import rrule, DAILY
from contextlib import suppress
import calendar

import numpy as np