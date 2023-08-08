import pytest
import importlib.metadata


@pytest.hookimpl()
def pytest_addoption(parser) -> None:
    group = parser.getgroup("maxcov", help=importlib.metadata.version("pytest-maxcov"))
