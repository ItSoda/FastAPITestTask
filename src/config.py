from dotenv import load_dotenv
import os


load_dotenv()

DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")

if os.environ.get("DOCKER_IS_RUN"):
    DB_HOST = "mysql_fastapi"
    DB_USER = "itsoda"
    DB_PASSWORD = "test_pass"