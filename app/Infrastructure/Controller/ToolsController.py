from flask import Blueprint, url_for
from flask import current_app

toolsController = Blueprint('toolsController', __name__)

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()

    return len(defaults) >= len(arguments)

@toolsController.route("/site-map")
def site_map_route():
    """Generate a site map of all routes in the application.
    Returns:
        list: A list of tuples containing the URL and endpoint for each route.
    """
    routes = []

    for rule in current_app.url_map.iter_rules():
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            routes.append((url, rule.endpoint))

    print(routes)
    return routes