from flask import url_for

from lib.tests import ViewTestMixin


class TestHealthy(ViewTestMixin):
    def test_healthy_response(self):
        """Should respond with a 200"""
        response = self.client.get(url_for('HealthyView:get'))
        assert response.status_code == 200
