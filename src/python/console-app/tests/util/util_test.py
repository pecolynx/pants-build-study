from console_app.util.util import now
import pendulum


def test_now():
    x = now()
    assert isinstance(x, pendulum.DateTime)

