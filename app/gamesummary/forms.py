from wtforms import Form, SelectField

from app import constants

class GameSummaryForm(Form):
    teamstrengths = SelectField(u'Team Strength', choices=constants.strength_situations)
    scoresituations = SelectField(u'Team Strength', choices=constants.strength_situations)
    period = SelectField(u'Team Strength', choices=constants.strength_situations)
    tablecolumns = SelectField(u'Team Strength', choices=constants.strength_situations)
