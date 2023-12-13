from decouple import Config

config = Config(".env")

if config.get("DOCKER_CONTAINER", default=None):
    config = Config("itsoda/docker-compose.env")

# PARAMETRS FOR DB
DB_HOST = config.get("MYSQL_HOST", default="localhost")
DB_USER = config.get("MYSQL_ROOT_USER", default="root")
DB_PASSWORD = config.get("MYSQL_ROOT_PASSWORD", default="nik140406")
DB_NAME = config.get("MYSQL_DATABASE", default="FastAPI_DB")
DB_PORT = config.get("MYSQL_PORT", default="3306")
