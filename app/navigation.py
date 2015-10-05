


def setup_nav():
	rd = {}
	teamDict ={
		'Anaheim Ducks': 'ANA', 'Arizona Coyotes': 'ARI',
		'Boston Bruins': 'BOS', 'Buffalo Sabres':'BUF',
		'Calgary Flames':'CGY', 'Carolina Hurricanes':'CAR',
		'Chicago Blackhawks':'CHI', 'Colorado Avalanche':'COL',
		'Columbus Blue Jackets':'CBJ', 'Dallas Stars':'DAL',
		'Detroit Red Wings':'DET', 'Edmonton Oilers':'EDM',
		'Florida Panthers':'FLA', 'Los Angeles Kings':'L.A',
		'Minnesota Wild':'MIN', 'Montreal Canadiens':'MTL',
		'Nashville Predators':'NSH', 'New Jersey Devils':'N.J',
		'New York Islanders':'NYI', 'New York Rangers':'NYR',
		'Philadelphia Flyers':'PHI', 'Pittsburgh Penguins':'PIT',
		'Ottawa Senators':'OTT', 'San Jose Sharks':'S.J',
		'St Louis Blues':'STL','Tampa Bay Lightning':'T.B',
		'Toronto Maple Leafs':'TOR', 'Vancouver Canucks':'VAN',
		'Washington Capitals':'WSH', 'Winnipeg Jets':'WPG'
	}
	atlantic = ['Boston Bruins', 'Buffalo Sabres', 'Detroit Red Wings',
		'Florida Panthers', 'Montreal Canadiens', 'Ottawa Senators',
		'Tampa Bay Lightning', 'Toronto Maple Leafs']
	atlDict = conferences(atlantic, teamDict)
	metropolitan = ['Carolina Hurricanes', 'Columbus Blue Jackets',
		'New Jersey Devils', 'New York Islanders',
		'New York Rangers', 'Philadelphia Flyers', 'Pittsburgh Penguins',
		'Washington Capitals']
	metDict = conferences(metropolitan, teamDict)
	central = ['Chicago Blackhawks', 'Colorado Avalanche', 'Dallas Stars',
		'Minnesota Wild', 'Nashville Predators', 'St Louis Blues', 'Winnipeg Jets']
	cenDict = conferences(central, teamDict)
	pacific = ['Anaheim Ducks', 'Arizona Coyotes', 'Calgary Flames',
		'Edmonton Oilers', 'Los Angeles Kings',
		'San Jose Sharks', 'Vancouver Canucks']
	pacDict = conferences(pacific, teamDict)

	rd["conferences"] = {
		"Eastern - Atlantic": atlDict,
		"Eastern - Metropolitan": metDict,
		"Western - Pacific": pacDict,
		"Western - Central": cenDict,
	}

	rd["teamDict"] = teamDict
	return rd


def conferences(conference, teamDict):
	cdict = {}
	for team in conference:
		cdict[team] = teamDict[team]
	return cdict
