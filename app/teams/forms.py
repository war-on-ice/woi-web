from wtforms import Form, SelectMultipleField, SelectField, BooleanField

from operator import itemgetter

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


class ComparisonForm(Form):
    startingSeason = SelectField(u'Starting Season',
        choices=[(20152015, 20152016), (20142015, 20142015),
                (20132014, 20142014)],
        default=[20152016])
    endingSeason = SelectField(u'Ending Season',
        choices=[(20152015, 20152016), (20142015, 20142015),
                (20132014, 20142014)],
        default=[20152016])
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
    # TODO: Check, some column choices seemed redundant
    tablecolumns = SelectField(u'Table Columns',
        choices=[("0", "Prime"), ("1", "High-Danger Chances"), ("2", "Scoring Chances"),
                ("3", "Corsi/Fenwick"), ("5", "Shot-Based/Goal-Based"),
                ("7", "Faceoffs"), ("9", "All")],
        default="0")
    splitgame = BooleanField(u'Split by Game')
    #daterange = BooleanField(u'Use Date Range')
    divideSeason = BooleanField(u'Divide Data By Season', default=True)


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
