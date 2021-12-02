from flask import url_for, render_template, request, session, Blueprint, abort

from app import db
from app.controllers.decorators import funcionario_required, admin_required, get_user_object

from app.models.relatorio import Relatorio
from app.models.funcionario import Funcionario