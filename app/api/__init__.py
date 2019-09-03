from flask_classful import FlaskView


class APIView(FlaskView):
    """
    Inherits from flask_classful.FlaskView
    Prefix the route with "/api"
    """
    route_prefix = "/api"