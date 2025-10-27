import snoop
import pendulum
import os
import pytest


@pytest.fixture(scope="session", autouse=True)
def timestamp():
    os.makedirs("logs", exist_ok=True)
    now = pendulum.now()
    timestamp_str = now.format("YYYY-MM-DD_HH-mm-ss")
    snoop.install(out=f"logs/{timestamp_str}.log")

    return timestamp_str
