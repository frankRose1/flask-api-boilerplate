import os
from datetime import timedelta
from distutils.util import strtobool

LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')

SECRET_KEY = os.getenv('SECRET_KEY', None)

SERVER_NAME = os.getenv('SERVER_NAME',
                        'localhost:{0}'.format(os.getenv('DOCKER_WEB_PORT',
                                                          '8000'))))

# SQLALchemy
pg_user = os.getenv('POSTGRES_USER', 'vidme')
pg_pass = os.getenv('POSTGRES_PASSWORD', 'password')
pg_host = os.getenv('POSTGRES_HOST', 'postgres')
pg_port = os.getenv('POSTGRES_PORT', '5432')
pg_db = os.getenv('POSTGRES_DB', pg_user)
db = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(pg_user, pg_pass,
                                               pg_host, pg_port, pg_db)
SQLALCHEMY_DATABASE_URI = db
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Seed user
SEED_ADMIN_EMAIL = os.getenv('SEED_ADMIN_EMAIL', 'dev@local.host')
SEED_ADMIN_PASSWORD = os.getenv('SEED_ADMIN_PASSWORD', 'password')
SEED_ADMIN_USERNAME = os.getenv('SEED_ADMIN_USERNAME', 'devAdmin1')

# Celery
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELEREY_REDIS_MAX_CONNECTIONS = 5

# Only allows JWT cookies to be sent over HTTPS
# In production this should be True
JWT_COOKIE_SECURE = False

# Expire access tokens in 1 year
JWT_ACCESS_TOKEN_EXPIRES = timedelta(weeks=52)