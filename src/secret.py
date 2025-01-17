import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from dotenv import load_dotenv

env_file = os.getenv("ENV_FILE_PATH", "env/.env.development")
if os.path.exists(env_file):
    load_dotenv(dotenv_path=env_file)
else:
    raise FileNotFoundError(f"Environment file not found: {env_file}")


class Config:
    NAS_USERNAME = os.getenv("NAS_USERNAME")
    NAS_PASSWORD = os.getenv("NAS_PASSWORD")
    NAS_PORT_1 = os.getenv("NAS_PORT_1")
    NAS_PORT_2 = os.getenv("NAS_PORT_2")
    NAS_IP_1 = os.getenv("NAS_IP_1")
    NAS_IP_2 = os.getenv("NAS_IP_2")
    NAS_IP_3 = os.getenv("NAS_IP_3")
    NAS_IP_4 = os.getenv("NAS_IP_4")
    NAS_IP_5 = os.getenv("NAS_IP_5")
    PGADMIN_EMAIL = os.getenv("PGADMIN_EMAIL")
    PGADMIN_PASSWORD = os.getenv("PGADMIN_PASSWORD")
    POSTGRESQL_USER = os.getenv("POSTGRESQL_USER")
    POSTGRESQL_PASSWORD = os.getenv("POSTGRESQL_PASSWORD")
    POSTGRESQL_DATABASE = os.getenv("POSTGRESQL_DATABASE")
    POSTGRESQL_HOST = os.getenv("POSTGRESQL_HOST")
    MIDDLEWARE_SECRET_KEY = os.getenv("MIDDLEWARE_SECRET_KEY")
    RABBITMQ_DEFAULT_USER = os.getenv("RABBITMQ_DEFAULT_USER")
    RABBITMQ_DEFAULT_PASS = os.getenv("RABBITMQ_DEFAULT_PASS")
    RABBITMQ_DEFAULT_HOST = os.getenv("RABBITMQ_DEFAULT_HOST")
    SYNC_PGSQL_CONNECTION = f"postgresql+psycopg2://{POSTGRESQL_USER}:{POSTGRESQL_PASSWORD}@{POSTGRESQL_HOST}/{POSTGRESQL_DATABASE}"
    ASYNC_PGSQL_CONNECTION = f"postgresql+asyncpg://{POSTGRESQL_USER}:{POSTGRESQL_PASSWORD}@{POSTGRESQL_HOST}/{POSTGRESQL_DATABASE}"
    PGSQL_BACKEND = f"db+postgresql://{POSTGRESQL_USER}:{POSTGRESQL_PASSWORD}@{POSTGRESQL_HOST}:5432/{POSTGRESQL_DATABASE}"
    BROKER_URL = f"amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@{RABBITMQ_DEFAULT_HOST}"
