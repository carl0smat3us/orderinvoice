from os import getenv
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from pytest import fixture
from api.main import app

load_dotenv()

@fixture
def client():
    return TestClient(app)

@fixture
def api_key_header():
    return {"x-api-key": getenv("API_KEY")}