from app import create_app
import pytest

@pytest.fixture(scope='module')
def test_client():
        app = create_app()
        app.config['WTF_CSRF_ENABLED'] = False

        with app.test_client() as client:
            with app.app_context():
                yield client
