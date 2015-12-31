from wtforms import Form, SelectField

from operator import itemgetter

from app import constants

class GameSummaryForm(Form):
    teamstrengths = SelectField(u'Team Strength',
        choices=sorted([(str(constants.strength_situations_dict[key]["value"]), key)
                        for key in constants.strength_situations_dict],
                        key=lambda k: constants.strength_situations_dict[k[1]]["order"]),
        default=constants.strength_situations_dict["Even strength 5v5"]["value"])
    scoresituations = SelectField(u'Score Situation',
        choices=sorted([(str(constants.score_situations_dict[key]["value"]), key)
                        for key in constants.score_situations_dict],
                        key=lambda k: constants.score_situations_dict[k[1]]["order"]),
        default=constants.score_situations_dict["All"]["value"])
    period = SelectField(u'Period',
        choices=sorted([(key, key)
                        for key in constants.periods_options],
                        key=lambda k: constants.periods_options[k[1]]["order"]),
        default=constants.periods["default"])
    tablecolumns = SelectField(u'Table Columns', choices=[("0", "Prime"), ("1", "Rates"),
                                                          ("2", "Counts"), ("3", "All")],
        default="0")


class SeriesSummaryForm(Form):
    teamstrengths = SelectField(u'Team Strength',
        choices=sorted([(str(constants.strength_situations_dict[key]["value"]), key)
                        for key in constants.strength_situations_dict],
                        key=lambda k: constants.strength_situations_dict[k[1]]["order"]),
        default=constants.strength_situations_dict["Even strength 5v5"]["value"])
    scoresituations = SelectField(u'Score Situation',
        choices=sorted([(str(constants.score_situations_dict[key]["value"]), key)
                        for key in constants.score_situations_dict],
                        key=lambda k: constants.score_situations_dict[k[1]]["order"]),
        default=constants.score_situations_dict["All"]["value"])
    period = SelectField(u'Period',
        choices=sorted([(key, key)
                        for key in constants.periods_options],
                        key=lambda k: constants.periods_options[k[1]]["order"]),
        default=constants.periods["default"])
    tablecolumns = SelectField(u'Table Columns', choices=[("0", "Prime"), ("1", "Rates"),
                                                          ("2", "Counts"), ("3", "All")],
        default="0")
    season = SelectField(choices=[(20152016, 20152016), (20142015, 20142015), (20132014, 20142014)],
        default=20152016)
    session = SelectField(choices=[("all", "Regular/Playoffs"), ("regular", "Regular"), ("playoffs", "Playoffs")],
        default="all")
    team1 = SelectField(choices=[(constants.teamDict[key], key) for key in constants.teamDict],
        default="TOR")
    team2 = SelectField(choices=[(constants.teamDict[key], key) for key in constants.teamDict],
        default="PIT")
