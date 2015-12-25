import flask
from datetime import datetime
from app.constants import teamDict, teamShortDict, comparisonchoices, standingsglossary

blueprint = flask.Blueprint('filters', __name__)


@blueprint.app_template_filter()
def format_currency(value):
    value = round(value,0)
    return "${:,.0f}".format(value)


@blueprint.app_template_filter()
def get_team_color(team, primary=True):
    for line in open("teamcolors.csv"):
        line = line.replace("\n", "").split(",")
        try:
            names = [line[1], line[4], line[5]]
            print names
            if team in names:
                if primary is True:
                    return line[2]
                else:
                    return line[3]
        except:
            pass


@blueprint.app_template_filter()
def tooltip_standings(column):
    return find_tooltip(column, standingsglossary)


@blueprint.app_template_filter()
def tooltip(column):
    return find_tooltip(column, comparisonchoices)


def find_tooltip(column, choices):
    for choice in choices:
        if choice[0] == column:
            return choice[1]
    print column
    return column


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
    try:
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
            seconds = str(int(60 - seconds))
            if len(seconds) == 1:
                seconds = "0" + seconds
            return str(int(19 - minutes)) + ":" + seconds + ", " + period
        return value.status
    except:
        if value["status"] == 3:
            if value["seconds"] > 3600:
                return "Final (OT)"
            return "Final"
        elif value["status"] == 4:
            return "Not Started"
        elif value["status"] == 2:
            ps = 0
            period = "1st"
            if value["seconds"] < 1200:
                ps = value["seconds"]
                period = "1st"
            elif value["seconds"] == 1200:
                return "End of 1st"
            elif value["seconds"] > 1200 and value["seconds"] < 2400:
                ps = value["seconds"] - 1200
                period = "2nd"
            elif value["seconds"] == 2400:
                return "End of 2nd"
            elif value["seconds"] > 2400 and value["seconds"] < 3600:
                ps = value["seconds"] - 2400
                period = "3rd"
            elif value["seconds"] == "3600":
                return "End of 3rd"
            else:
                ps = value["seconds"] - 3600
                period = "OT"
            minutes, seconds = divmod(ps, 60)
            seconds = str(int(60 - seconds))
            if len(seconds) == 1:
                seconds = "0" + seconds
            return str(int(19 - minutes)) + ":" + seconds + ", " + period
        return value["status"]
