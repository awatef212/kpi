import os

from dotenv import load_dotenv

load_dotenv()

PROCESS = os.getenv('ENV_PROCESS')

MYSQL_DB_HOST = os.getenv("ENV_MYSQL_DB_HOST")
MYSQL_DB_USER = os.getenv("ENV_MYSQL_DB_USER")
MYSQL_DB_PASSWORD = os.getenv("ENV_MYSQL_DB_PASSWORD")
MYSQL_DB_NAME = os.getenv("ENV_MYSQL_DB_NAME")
