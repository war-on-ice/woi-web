from flask import Flask, render_template, send_from_directory
app = Flask(__name__)


@app.route("/")
def index():
	return render_template("index.html")


@app.route("/iframe")
def iframe_test():
	return render_template("iframe_test.html")

@app.route("/r/<string:pagename>/")
def iframe_woi(pagename):
	return render_template("woi-frame.html", page = pagename)

@app.route("/cap/team/<string:team>/")
def iframe_cap_team(team):
	teamDict ={
		'Anaheim Ducks': 'ANA','Arizona Coyotes': 'ARI','Boston Bruins': 'BOS','Buffalo Sabres':'BUF',
				  'Calgary Flames':'CGY','Carolina Hurricanes':'CAR','Chicago Blackhawks':'CHI','Colorado Avalanche':'COL',
				  'Columbus Blue Jackets':'CBJ','Dallas Stars':'DAL','Detroit Red Wings':'DET','Edmonton Oilers':'EDM',
				  'Florida Panthers':'FLA','Los Angeles Kings':'L.A','Minnesota Wild':'MIN','Montreal Canadiens':'MTL',
				  'Nashville Predators':'NSH','New Jersey Devils':'N.J','New York Islanders':'NYI','New York Rangers':'NYR',
				  'Philadelphia Flyers':'PHI','Pittsburgh Penguins':'PIT','Ottawa Senators':'OTT','San Jose Sharks':'S.J',
				  'St Louis Blues':'STL','Tampa Bay Lightning':'T.B','Toronto Maple Leafs':'TOR','Vancouver Canucks':'VAN',
				  'Washington Capitals':'WSH','Winnipeg Jets':'WPG'
	}
	return render_template("woi-frame.html", page = teamDict[team])


@app.route("/dummydata/<string:filename>")
def dummy_path(filename):
	return send_from_directory('dummydata', filename)



if __name__ == "__main__":
	app.run("0.0.0.0", debug=True)
