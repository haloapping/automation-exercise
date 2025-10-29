import snoop
import pendulum
import os

TIMESTAMP = None

def pytest_sessionstart(session):
    global TIMESTAMP

    os.makedirs("logs", exist_ok=True)

    now = pendulum.now()
    timestamp_str = now.format("YYYY-MM-DD_HH-mm-ss")
    TIMESTAMP = timestamp_str

    snoop.install(out=f"logs/{timestamp_str}.log")
