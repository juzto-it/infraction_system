import pymysql
import os
pymysql.install_as_MySQLdb()
import environ
env = environ.Env()
ENV_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env.read_env(os.path.join('../',ENV_DIR, '.env'))