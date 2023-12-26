'''Module app'''
from os import getenv
import os
from flask import Flask

dir_path = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__, root_path=dir_path)
app.secret_key = getenv("SECRET_KEY")

import routes
