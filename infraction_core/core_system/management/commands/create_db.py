# polls/management/commands/create_db.py
import sys
import logging
import MySQLdb

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

rds_host = settings.env('DB_SERVER')
db_name = settings.env('DB_SCHEMA')
user_name = settings.env('DB_USER')
password = settings.env('DB_PASS')
port = settings.env('DB_PORT')

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Command(BaseCommand):
    help = 'Creates the initial database'

    def handle(self, *args, **options):
        print('Starting db creation')
        try:
            db = MySQLdb.connect(host=rds_host, user=user_name,
                                 password=password, db="mysql", connect_timeout=5)
            c = db.cursor()
            print("connected to db server")
            c.execute("""CREATE DATABASE pollsdb;""")
            c.execute(
                """GRANT ALL PRIVILEGES ON db_name.* TO 'polls_admin' IDENTIFIED BY 'pollsadmin';""")
            c.close()
            print("closed db connection")
        except:
            logger.error(
                "ERROR: Unexpected error: Could not connect to MySql instance.")
            sys.exit()