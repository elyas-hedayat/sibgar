import os
from config.env import env, BASE_DIR

env.read_env(os.path.join(BASE_DIR, ".env.production"))

DEBUG = False

SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])
