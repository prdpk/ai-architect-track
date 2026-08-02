from unittest.mock import MagicMock
import pytest
import app.main as main_module


@pytest.fixture(autouse=True)
def mock_redis(monkeypatch):
    """Patch the Redis client for all tests so tests never touch real Redis."""
    fake = MagicMock()
    fake.get.return_value = None   # always cache miss — tests hit the backend
    fake.set.return_value = True
    monkeypatch.setattr(main_module, "redis_client", fake)
