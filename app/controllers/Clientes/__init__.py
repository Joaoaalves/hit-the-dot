from app import db, app
from app.controllers.decorators import admin_required, funcionario_required, get_user_object, gestor_required
from flask import Blueprint, request, render_template, redirect, url_for, abort, session

from app.models.cliente import Cliente

from app.controllers.Login.utils import get_secure_file