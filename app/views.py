from app.navigation import setup_nav
from flask import Blueprint, render_template


from gamesummary import calls


mod = Blueprint('app', __name__)


@mod.route("/")
def index():
    rd = setup_nav()
    games = calls.get_games()
    return render_template("index.html", rd=rd,
        games=games)


@mod.route("/iframe")
def iframe_test():
    rd = setup_nav()
    return render_template("iframe_test.html", rd=rd)


@mod.route("/r/<string:pagename>/")
def iframe_woi(pagename):
    rd = setup_nav()
    print pagename
    return render_template("woi-frame.html", page=pagename, rd=rd,
        url="http://biscuit.war-on-ice.com/" + pagename)


@mod.route("/cap/")
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


@mod.route("/glossary/")
def glossary():
    rd = setup_nav()
    return render_template("misc/glossary.html", rd = rd)


@mod.route("/about/")
def about():
    rd = setup_nav()
    return render_template("misc/about.html", rd = rd)