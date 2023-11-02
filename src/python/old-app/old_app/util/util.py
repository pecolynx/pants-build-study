import pendulum
from pendulum.datetime import DateTime


def now() -> DateTime:
    return pendulum.now("Europe/Paris")
