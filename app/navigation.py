from constants import teamDict


def setup_nav():
	rd = {}
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
		"East - Atlantic": atlDict,
		"East - Metropolitan": metDict,
		"West - Pacific": pacDict,
		"West - Central": cenDict,
	}

	rd["teamDict"] = teamDict
	return rd


def conferences(conference, teamDict):
	cdict = {}
	for team in conference:
		cdict[team] = teamDict[team]
	return cdict
