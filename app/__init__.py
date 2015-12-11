from flask import Flask, send_from_directory
import filters
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.moment import Moment
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

from config import contractConnStr


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
moment = Moment(app)

Base = declarative_base()
Base.metadata.reflect(bind = db.engine, views = True)

capengine = create_engine(contractConnStr)
CapBase = declarative_base()
CapBase.metadata.reflect(bind=capengine, views=True)

# Register blueprints

from app.cap.views import mod as capModule
from app.gamesummary.views import mod as gameSummaryModule
from views import mod as appModule
app.register_blueprint(capModule)
app.register_blueprint(appModule)
app.register_blueprint(gameSummaryModule)
app.register_blueprint(filters.blueprint)
