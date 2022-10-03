from flask import Blueprint, render_template, redirect, request, url_for, session, abort
from app.controllers.decorators import login_required, admin_required, gestor_required, get_user_object, funcionario_required, is_gestor, is_func
from app.controllers.Login.utils import get_secure_file

from app import db, app, limiter

from datetime import datetime
from contextlib import suppress

from app.models.servico_entregue import ServicoEntregue
from app.models.servico import Servico

import json
