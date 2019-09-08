from flask_classful import FlaskView


class HealthyView(FlaskView):
    def get(self):
        """Send back a 200 for health checks"""
        return '', 200
