from app import db

import flask

from flask import Blueprint, url_for, render_template, redirect, request, abort, session

from app.controllers.decorators import funcionario_required, admin_required, is_admin, get_user_object

from app.models.funcionario import Funcionario

from datetime import datetime, timedelta

import time