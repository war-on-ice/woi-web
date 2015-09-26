from flask import Flask, render_template, send_from_directory
import filters
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

Base = declarative_base()
Base.metadata.reflect(bind = db.engine, views = True)

from app.navigation import setup_nav

@app.route("/")
def index():
	rd = setup_nav()
	return render_template("index.html", rd=rd)


@app.route("/iframe")
def iframe_test():
	rd = setup_nav()
	return render_template("iframe_test.html", rd=rd)

@app.route("/r/<string:pagename>/")
def iframe_woi(pagename):
	rd = setup_nav()
	print pagename
	return render_template("woi-frame.html", page=pagename, rd=rd,
		url="http://biscuit.war-on-ice.com/" + pagename)

@app.route("/cap/")
def iframe_cap():
	rd = setup_nav()
	endurls = [("quicksheet", "Quick Look"),
				("recent-signings", "Recent Signings"),
				("playerroster", "Player AAV By Season"),
				("attained-bonuses", "Performance Bonuses Attained")]
	urls = []
	for u in endurls:
		tu = {}
		tu["id"] = u[0]
		tu["name"] = u[1]
		tu["url"] = "http://www.war-on-ice.com/cap/" + u[0] + ".html"
		urls.append(tu)
	rd["urls"] = urls
	return render_template("iframe_cap.html", cap=True, rd=rd)

# @app.route("/cap/team/<string:team>/")
# def iframe_cap_team(team):
# 	rd = setup_nav()
# 	return render_template("woi-frame.html", page=team, rd=rd,
# 		url="http://biscuit.war-on-ice.com/" + team + ".html")

@app.route("/dummydata/<string:filename>")
def dummy_path(filename):
	return send_from_directory('dummydata', filename)

from app.cap.views import mod as capModule
app.register_blueprint(capModule)

app.register_blueprint(filters.blueprint)
#
# filters.define_filters()