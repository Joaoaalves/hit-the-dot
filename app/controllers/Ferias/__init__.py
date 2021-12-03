from flask import render_template, redirect, url_for, Blueprint, session, request
from app.controllers.decorators import admin_required, funcionario_required, get_user_object