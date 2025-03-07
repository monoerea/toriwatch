import pytest
import asyncio

@pytest.fixture(scope="session")
def event_loop():
    """Ensure a new event loop is used for tests."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()
