import flask

blueprint = flask.Blueprint('filters', __name__)

@blueprint.app_template_filter()
def format_currency(value):
    value = round(value,0)
    return "${:,.0f}".format(value)