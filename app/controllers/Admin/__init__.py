from asyncio.log import logger
from app import app, db, users, invalid_sessions, app
import flask
from flask import Blueprint, render_template, redirect, url_for, request, session, abort

from app.controllers.decorators import get_user_object, admin_required, block_cross_site_requests

from app.models.funcionario import Funcionario
from app.models.turno import Turno

from datetime import datetime, date
from workalendar.america import BrazilDistritoFederal