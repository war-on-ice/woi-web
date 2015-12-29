from wtforms import Form, SelectMultipleField, SelectField, BooleanField, validators
from wtforms.validators import NumberRange
from wtforms.fields.html5 import DateField, IntegerRangeField

from operator import itemgetter

import datetime

from app import constants

class SeasonSelectForm(Form):
    seasons = SelectMultipleField(choices=[(20152016, 20152016), (20142015, 20142015), (20132014, 20142014)], default=[20152016])

    def __init__(self, formdata=None, obj=None, prefix='', **kwargs):
        try:
            kwargs.setdefault('season', kwargs["season_default"])
            print kwargs
        except:
            pass
        Form.__init__(self, formdata, obj, prefix, **kwargs)


class HistoryForm(Form):
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
    homeAway = SelectField(u'Home/Away Situation',
        choices=[("1", "Home"), ("0", "Away"), ("all", "All")],
        default="all")
    filterTeams = SelectField(u'Select Team',
        choices=sorted([(constants.teamDict[key], key) for key in constants.teamDict]),
        default="BOS")
    tablecolumns = SelectField(u'Table Columns',
        choices=[("0", "Prime"), ("1", "High-Danger Chances"), ("2", "Scoring Chances"),
                ("3", "Corsi/Fenwick"), ("5", "Shot-Based/Goal-Based"),
                ("7", "Faceoffs"), ("9", "All")],
        default="0")
    startingDate = DateField(u'Starting Date', validators=[validators.optional(),],
        default=datetime.datetime.strptime("2002-10-01", "%Y-%m-%d"))
    endingDate = DateField(u'Ending Date', validators=[validators.optional(),])
    regularplayoffs = SelectField(u'Regular/Playoffs',
        choices=[("0", "All"), ("1", "Regular"), ("2", "Playoff")],
        default="0")


class ComparisonForm(Form):
    startingSeason = SelectField(u'Starting Season',
        choices=[(20152015, 20152016), (20142015, 20142015),
                (20132014, 20142014)],
        default=[20152016])
    endingSeason = SelectField(u'Ending Season',
        choices=[(20152015, 20152016), (20142015, 20142015),
                (20132014, 20142014)],
        default=[20152016])
    startingDate = DateField(u'Starting Date', validators=[validators.optional(),])
    endingDate = DateField(u'Ending Date', validators=[validators.optional(),])
    homeAway = SelectField(u'Home/Away Situation',
        choices=[("1", "Home"), ("0", "Away"), ("all", "All")],
        default="all")

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
    tablecolumns = SelectField(u'Table Columns',
        choices=[("0", "Prime"), ("1", "High-Danger Chances"), ("2", "Scoring Chances"),
                ("3", "Corsi/Fenwick"), ("5", "Shot-Based/Goal-Based"),
                ("7", "Faceoffs"), ("9", "All")],
        default="0")
    splitgame = BooleanField(u'Split by Game')
    bydate = BooleanField(u'Use Date Range')
    divideSeason = BooleanField(u'Divide Data By Season', default=True)
    filterTeams = SelectMultipleField(u'Filter By Teams',
        choices=sorted([(constants.teamDict[key], key) for key in constants.teamDict]))


class ComparisonGraphForm(Form):
    xaxis = SelectField(u'X Axis Variable',
        choices=constants.comparisonchoices,
        default="ZSO%")
    yaxis = SelectField(u'Y Axis Variable',
        choices=constants.comparisonchoices,
        default="G+/-")
    caxis = SelectField(u'Color Variable',
        choices=constants.comparisonchoices,
        default="PDO")
    saxis = SelectField(u'Size Variable',
        choices=constants.comparisonchoices,
        default="FO%")


class GameGraphForm(Form):
    paxis = SelectField(u'X Axis Variable',
        choices=constants.comparisonchoices,
        default="SF")
    saxis = SelectField(u'Y Axis Variable', choices=constants.comparisonchoices + [("NA", "None"),], default="NA")
    steam = SelectMultipleField(u'Comparison Team',
        choices=sorted([(constants.teamDict[key], key) for key in constants.teamDict]))
    maverage = IntegerRangeField(u'Number of Games in Moving Average',
        default=25, validators=[NumberRange(1, 50)])
