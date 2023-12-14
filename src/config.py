from decouple import RepositoryEnv, Config
import os

docker = os.environ.get("DOCKER_CONTAINER")

env_file = ".env"

if docker:
    env_file = "docker-compose.env"
config = Config(RepositoryEnv(env_file))

# PARAMETRS FOR DB
print(config.get("MYSQL_HOST", default="localhosttt"))
DB_HOST = config.get("MYSQL_HOST", default="localhost")
DB_USER = config.get("MYSQL_ROOT_USER", default="root")
DB_PASSWORD = config.get("MYSQL_ROOT_PASSWORD", default="nik140406")
DB_NAME = config.get("MYSQL_DATABASE", default="FastAPI_DB")
DB_PORT = config.get("MYSQL_PORT", default="3306")
