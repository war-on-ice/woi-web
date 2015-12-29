def create_dict(dictionary):
    return {'options': sorted(dictionary.items(), key=lambda x: x[1]['order']),
                    'default': filter(lambda item: item[1]['default'] == 1, dictionary.items())[0][0]}

# Score Situations
score_situations_dict = {"Trailing by 3+": {'value': 0, 'order': 5, 'default': 0},
                    "Trailing by 2": {'value': 1, 'order': 7, 'default': 0},
                    "Trailing by 1": {'value': 2, 'order': 8, 'default': 0},
                    "Tied": {'value': 3, 'order': 9, 'default': 0},
                    "Leading by 1": {'value': 4, 'order': 11, 'default': 0},
                    "Leading by 2": {'value': 5, 'order':12, 'default': 0},
                    "Leading by 3+": {'value': 6, 'order': 14, 'default': 0},
                    "All": {'value': 7, 'order': 0, 'default': 1},
                    "All, score adjusted": {'value': 8, 'order': 1, 'default': 0},
                    "Within 1": {'value': 9, 'order': 3, 'default': 0},
                    "Close": {'value': 10, 'order': 2, 'default': 0},
                    "Leading": {'value': 11, 'order': 10, 'default': 0},
                    "Leading by 2+": {'value': 12, 'order': 13, 'default': 0},
                    "Trailing by 2+": {'value': 13, 'order': 6, 'default': 0},
                    "Trailing": {'value': 14, 'order': 4, 'default': 0}}

score_situations = create_dict(score_situations_dict)


# Strength Situations
strength_situations_dict = {"All": {'value': 7, 'order': 2, 'default': 0},
                      "Even strength 5v5": {'value': 1, 'order': 1, 'default': 1},
                      "Power play": {'value': 2, 'order': 3, 'default': 0},
                      "Shorthanded": {'value': 3, 'order': 4, 'default': 0},
                      "4v4": {'value': 4, 'order': 5, 'default': 0},
                      "Opposing goalie pulled": {'value': 5, 'order': 6, 'default': 0},
                      "Team goalie pulled": {'value': 6, 'order': 7, 'default': 0},
                      "Leftovers": {'value': 0, 'order': 8, 'default': 0}}

strength_situations = create_dict(strength_situations_dict)

# Positions
all_pos = ["C", "CR", "RC", "L", "CL", "LC", "CD", "DC", "RL", "LR",
           "RD", "DR", "LD", "DL", "D", "CD", "DC"]

positions_options = {"All": all_pos,
             "Center": filter(lambda pos: pos.find("C") > 0 , all_pos),
             "Left Wing": filter(lambda pos: pos.find("L") > 0 , all_pos),
             "Right Wing": filter(lambda pos: pos.find("R") > 0 , all_pos),
             "All Forwards": filter(lambda pos: pos.find("L") > 0 or pos.find("R") > 0 or pos.find("C") > 0 , all_pos),
             "Defense": filter(lambda pos: pos.find("D") > 0 , all_pos)}

positions_default = "All"

positions = {"options": positions_options,
             "default": positions_default}

# Game Periods
all_periods = [1,2,3,4,5,6,7] #assumes max 4 OTs

periods_options = {"1": {'value': filter(lambda pd: pd == 1, all_periods), 'order': 2, 'default': 0},
           "2": {'value': filter(lambda pd: pd == 2, all_periods), 'order': 3, 'default': 0},
           "3": {'value': filter(lambda pd: pd == 3, all_periods), 'order': 4, 'default': 0},
           "Regulation": {'value': filter(lambda pd: pd <= 3, all_periods), 'order': 5, 'default': 0},
           "Overtime": {'value': filter(lambda pd: pd >= 4, all_periods), 'order': 6, 'default': 0},
           "1st OT": {'value': filter(lambda pd: pd == 4, all_periods), 'order': 7, 'default': 0},
           "2nd OT": {'value': filter(lambda pd: pd == 5, all_periods), 'order': 8, 'default': 0},
           "3rd OT": {'value': filter(lambda pd: pd == 6, all_periods), 'order': 9, 'default': 0},
           "4th OT": {'value': filter(lambda pd: pd == 7, all_periods), 'order': 10, 'default': 0},
           "All": {'value': [0] + all_periods, 'order': 1, 'default': 1}}

periods = create_dict(periods_options)

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

teamShortDict ={
  'Ducks': 'ANA', 'Coyotes': 'ARI',
  'Coyotes (PHX)': 'PHX',
  'Bruins': 'BOS', 'Sabres':'BUF',
  'Flames':'CGY', 'Hurricanes':'CAR',
  'Blackhawks':'CHI', 'Avalanche':'COL',
  'Blue Jackets':'CBJ', 'Stars':'DAL',
  'Red Wings':'DET', 'Oilers':'EDM',
  'Panthers':'FLA', 'Kings':'L.A',
  'Wild':'MIN', 'Canadiens':'MTL',
  'Predators':'NSH', 'Devils':'N.J',
  'Islanders':'NYI', 'Rangers':'NYR',
  'Flyers':'PHI', 'Penguins':'PIT',
  'Senators':'OTT', 'Sharks':'S.J',
  'Blues':'STL','Lightning':'T.B',
  'Maple Leafs':'TOR', 'Canucks':'VAN',
  'Capitals':'WSH', 'Jets':'WPG'
}

standingsglossary = [("RW", "Regulation Wins"),
  ("OW", "Overtime Wins"),
  ("SW", "Shootout Wins"),
  ("RL", "Regulation Losses"),
  ("OL", "Overtime Losses"),
  ("SL", "Shootout Losses"),
  ("GF", "Goals For"),
  ("GA", "Goals Against"),
  ("CF", "Corsi For"),
  ("CA", "Corsi Against"),
  ("PNow", "Points, Under Current System"),
  ("P3", "Points, 3-2-1-0 System"),
  ("PTie", "Points, Tie After Overtime Ends"),
  ("PNL", "Points, No Tie or Loser Points")]

comparisonchoices = [("ZSN", "Neutral Zone Starts"),
  ("ZSO", "Offensive Zone Starts"),
  ("ZSD", "Defensive Zone Starts"),
  ("ZSO%", "Fraction of Off vs Def Zone Starts"),
  ("PDO", "PDO (On-Ice SvPct plus On-Ice ShPct)"),
  ("CF", "Corsi For Total"),
  ("CA", "Corsi Against Total"),
  ("C+/-", "On-Ice Corsi Differential"),
  ("CF%", "Corsi For Percentage of Total"),
  ("CF60", "Corsi For, Per 60 Minutes"),
  ("CA60", "Corsi Against, Per 60 Minutes"),
  ("CP60", "Corsi Events, For And Against, Per 60 Minutes"),
  ("FF", "Fenwick For Total"),
  ("FA", "Fenwick Against Total"),
  ("F+/-", "On-Ice Fenwick Differential"),
  ("FF%", "Fenwick For Percentage of Total"),
  ("FF60", "Fenwick For, Per 60 Minutes"),
  ("FA60", "Fenwick Against, Per 60 Minutes"),
  ("FP60", "Fenwick Events, For And Against, Per 60 Minutes"),
  ("SA", "On-Ice Shots-On-Goal Against Total"),
  ("S+/-", "On-Ice Shots-On-Goal Differential"),
  ("SF%", "On-Ice Shots-On-Goal For Share of Total"),
  ("SF60", "On-Ice Shots-On-Goal For, Per 60 Minutes"),
  ("SA60", "On-Ice Shots-On-Goal Against, Per 60 Minutes"),
  ("GF", "On-Ice Goals For Total"),
  ("GA", "On-Ice Goals Against Total"),
  ("G+/-", "On-Ice Goal Differential"),
  ("GF%", "On-Ice Goals For Percentage of Total"),
  ("GF60", "On-Ice Goals For, Per 60 Minutes"),
  ("GA60", "On-Ice Goals Against, Per 60 Minutes"),
  ("SCF", "On-Ice Scoring Chances For Total"),
  ("SCA", "On-Ice Scoring Chances Against Total"),
  ("SC+/-", "On-Ice Scoring Chances Differential"),
  ("SCF%", "On-Ice Scoring Chances For Percentage of Total"),
  ("SCF60", "On-Ice Scoring Chances For, Per 60 Minutes"),
  ("SCA60", "On-Ice Scoring Chances Against, Per 60 Minutes"),
  ("SCP60", "On-Ice Scoring Chances, For And Against, Per 60 Minutes"),
  ("HSCF", "On-Ice High-Danger Scoring Chances For Total"),
  ("HSCA", "On-Ice High-Danger Scoring Chances Against Total"),
  ("HSC+/-", "On-Ice High-Danger Scoring Chances Differential"),
  ("HSCF%", "On-Ice High-Danger Scoring Chances For Percentage of Total"),
  ("HSCF60", "On-Ice High-Danger Scoring Chances For, Per 60 Minutes"),
  ("HSCA60", "On-Ice High-Danger Scoring Chances Against, Per 60 Minutes"),
  ("HSCP60", "On-Ice High-Danger Scoring Chances, For And Against, Per 60 Minutes"),
  ("FO_W", "Faceoffs Won"),
  ("FO_L", "Faceoffs Lost"),
  ("FO%", "Faceoff Winning Percentage"),
  ("TOI", "Time On Ice"),
  ("PN", "Penalties"),
  ("PN-", "Penalties Drawn"),
  ("PenD", "Penalty Differential"),
  ("PenD60", "Penalty Differential per 60"),
  ("HIT", "Hits"),
  ("HIT-", "Hits Taken"),
  ("MSF", "Missed Shots For"),
  ("MSA", "Missed Shots Against"),
  ("BSF", "Blocked Shots"),
  ("BSA", "Shot Attempts Blocked"),
  ("SF", "On-Ice Shot Attempts On Goal"),
  ("OFOn%", "On-Ice Unblocked Shot Attempts On Goal"),
  ("OSh%", "On-Ice Shooting Percentage"),
  ("OFenSh%", "On-Ice Unblocked Shooting Percentage"),
  ("OCOn%", "On-ice Corsi On-goal Percentage"),
  ("OFAOn%", "On-Ice Unblocked Shot Attempts On Goal, Against"),
  ("OSv%", "On-Ice Save Percentage"),
  ("FenSv%", "On-Ice Unblocked Save Percentage"),
  ("season", "Time")]
