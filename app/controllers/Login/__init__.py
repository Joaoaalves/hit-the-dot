from app import app, invalid_sessions, users, invalid_sessions, db
from app.controllers.decorators import block_cross_site_requests, login_required, admin_required, is_admin, get_user_object
from flask import Blueprint, request, url_for, render_template, redirect, session
import flask
import random
from password_strength import PasswordPolicy, PasswordStats
import re
import os
from subprocess import Popen

from app.utils.phoneValidator import *