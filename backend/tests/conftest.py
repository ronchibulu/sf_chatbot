"""Pytest configuration and shared fixtures."""
import pytest


@pytest.fixture
def test_config():
    """Fixture providing test configuration."""
    return {
        "database_url": "postgresql+psycopg://user:password@localhost:5432/sleekflow_db",
        "secret_key": "test-secret-key"
    }
