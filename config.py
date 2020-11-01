import os
SECRET_KEY = 'v}*`KT3:82^dc[|M?.rYs/)QP#:2Bf*0M#WaG"$aq.iPMnA_vph&5=RL;_e"|Br'
SESSION_TYPE = 'filesystem'
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(basedir, 'sica.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False