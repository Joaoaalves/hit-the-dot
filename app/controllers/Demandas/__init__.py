from flask import Blueprint, render_template, redirect, request, url_for, session, abort
from app.controllers.decorators import login_required, admin_required, gestor_required, get_user_object, funcionario_required
from app.controllers.Login.utils import get_secure_file

from app import db, app

from datetime import datetime
from contextlib import suppress

from app.models.demanda import Demanda
from app.models.servico_atribuido import ServicoAtribuido
