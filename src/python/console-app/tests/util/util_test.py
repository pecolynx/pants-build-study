import pendulum
from console_app.util.util import now


def test_now():
    x = now()
    assert isinstance(x, pendulum.DateTime)
