from app import db
from app.controllers.decorators import admin_required, funcionario_required, get_user_object
from flask import Blueprint, request, render_template, redirect, url_for, abort, session

from app.models.cliente import Cliente