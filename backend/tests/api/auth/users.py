import pytest
from fastapi.testclient import TestClient
from backend.api.main import app

client = TestClient(app)

