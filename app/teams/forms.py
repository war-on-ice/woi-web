from wtforms import Form, SelectMultipleField

from operator import itemgetter

from app import constants

class SeasonSelectForm(Form):
    seasons = SelectMultipleField(choices=[(20152016, 20152016), (20142015, 20142015), (20132014, 20142014)], default=[20152015])

    def __init__(self, formdata=None, obj=None, prefix='', **kwargs):
        try:
            kwargs.setdefault('season', kwargs["season_default"])
            print kwargs
        except:
            pass
        Form.__init__(self, formdata, obj, prefix, **kwargs)