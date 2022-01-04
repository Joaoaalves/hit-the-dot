from flask import Blueprint, render_template, redirect, url_for, session, request
from app import db
from app.controllers.decorators import admin_required, funcionario_required, get_user_object

# Models
from app.models.falta import Falta