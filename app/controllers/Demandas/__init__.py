from flask import Blueprint, render_template, redirect, request, url_for, session, abort
from app.controllers.decorators import login_required, admin_required, gestor_required, get_user_object, funcionario_required
from app import db

from datetime import datetime
from contextlib import suppress

from app.models.demanda import Demanda