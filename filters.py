import flask
from datetime import datetime
from app.constants import teamDict
from app.constants import teamShortDict

blueprint = flask.Blueprint('filters', __name__)


@blueprint.app_template_filter()
def format_currency(value):
    value = round(value,0)
    return "${:,.0f}".format(value)

@blueprint.app_template_filter()
def format_date(value):
    dateObj = datetime.strptime(value, "%Y-%m-%d")
    return dateObj.strftime('%b %-d, %Y')

@blueprint.app_template_filter()
def teamname(value):
    for team in teamDict:
        if teamDict[team] == value:
            return team
    return value

@blueprint.app_template_filter()
def teamshortname(value):
    for team in teamShortDict:
        if teamShortDict[team] == value:
            return team
    return value

@blueprint.app_template_filter()
def get_status(value):
    if value.status == 3:
        if value.seconds > 3600:
            return "Final (OT)"
        return "Final"
    elif value.status == 4:
        return "Not Started"
    elif value.status == 2:
        ps = 0
        period = "1st"
        if value.seconds < 1200:
            ps = value.seconds
            period = "1st"
        elif value.seconds == 1200:
            return "End of 1st"
        elif value.seconds > 1200 and value.seconds < 2400:
            ps = value.seconds - 1200
            period = "2nd"
        elif value.seconds == 2400:
            return "End of 2nd"
        elif value.seconds > 2400 and value.seconds < 3600:
            ps = value.seconds - 2400
            period = "3rd"
        elif value.seconds == "3600":
            return "End of 3rd"
        else:
            ps = value.seconds - 3600
            period = "OT"
        minutes, seconds = divmod(ps, 60)
        return str(int(19 - minutes)) + ":" + str(int(60 - seconds)) + ", " + period
    return value.status
