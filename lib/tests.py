import pytest


class ViewTestMixin(object):
    """
    Automatically load in a session and client
    """
    @pytest.fixture(autouse=True)
    def set_common_fixtures(self, session, client):
        self.session = session
        self.client = client
