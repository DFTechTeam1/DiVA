from dotenv import load_dotenv


def pytest_configure():
    load_dotenv(dotenv_path="env/.env.testing")
