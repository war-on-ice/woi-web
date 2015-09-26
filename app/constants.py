# Score Situations
score_situations_options = {"Trailing By 3+": 0,
                    "Trailing By 2": 1,
                    "Trailing By 1": 2,
                    "Tied": 3,
                    "Leading By 1": 4,
                    "Leading By 2": 5,
                    "Leading By 3+": 6,
                    "All": 7,
                    "All, Score Adjusted": 8,
                    "Within 1": 9,
                    "Close": 10,
                    "Leading": 11,
                    "Leading By 2+": 12,
                    "Trailing By 2+": 13,
                    "Trailing": 14}
score_situation_default = "All"

score_situations = {"options": score_situations_options,
                    "default": score_situation_default}


# Strength Situations
strength_situations_options = {"All": 7,
                      "Even Strength 5v5": 1,
                      "Power Play": 2,
                      "Shorthanded": 3,
                      "4v4": 4,
                      "Opposing Goalie Pulled": 5,
                      "Team Goalie Pulled": 6,
                      "Leftovers": 0}
strength_situations_default = "Even Strength 5v5"

strength_situations = {"options": strength_situations_options,
                       "default": strength_situations_default}

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

periods_options = {"1": filter(lambda pd: pd == 1, all_periods),
           "2": filter(lambda pd: pd == 2, all_periods),
           "3": filter(lambda pd: pd == 3, all_periods),
           "Regulation": filter(lambda pd: pd <= 3, all_periods),
           "Overtime": filter(lambda pd: pd >= 4, all_periods),
           "1 OT": filter(lambda pd: pd == 4, all_periods),
           "2 OT": filter(lambda pd: pd == 5, all_periods),
           "3 OT": filter(lambda pd: pd == 6, all_periods),
           "4 OT": filter(lambda pd: pd == 7, all_periods),
           "All": all_periods}

periods_default = "All"

periods = {"options": periods_options,
           "default": periods_default}