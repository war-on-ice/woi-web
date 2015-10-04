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
           "All": {'value': all_periods, 'order': 1, 'default': 1}}

periods = create_dict(periods_options)