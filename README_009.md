## 9. Test

https://www.pantsbuild.org/docs/reference-pytest


### Add test code

```shell
mkdir -p src/python/console-app/tests/util
```

```python
cat <<EOF > src/python/console-app/tests/util/util_test.py
from console_app.util.util import now
import pendulum


def test_now():
    x = now()
    assert isinstance(x, pendulum.DateTime)
EOF
```

### Update pants.toml

Add the below codes to `pants.toml` file.

```toml
[test]
use_coverage = true

[coverage-py]
report = "xml"
```


```toml
cat <<EOF > pants.toml
[GLOBAL]
pants_version = "2.17.0"

backend_packages = [
    "pants.backend.python",
    "pants.backend.python.lint.bandit",
    "pants.backend.python.lint.black",
    "pants.backend.python.lint.docformatter",
    "pants.backend.docker.lint.hadolint",
    "pants.backend.python.lint.isort",
    "pants.backend.python.lint.pylint",
    "pants.backend.python.lint.pyupgrade",
    "pants.backend.experimental.python.lint.ruff",
    "pants.backend.python.typecheck.mypy",
    "pants.backend.codegen.protobuf.python",
    "pants.backend.docker",
]

[python]
interpreter_constraints = [">=3.11,<3.12"]
enable_resolves = true
default_resolve = "default"

[python.resolves]
default = "3rdparty/python/default.lock"
mypy = "3rdparty/python/mypy.lock"
pytext = "3rdparty/python/pytest.lock"
old_app = "3rdparty/python/old_app.lock"
grpc_client = "3rdparty/python/grpc_client.lock"

[source]
root_patterns = [
    "/src/python/*",
    "/src/protos",
]

[test]
use_coverage = true

[coverage-py]
report = "xml"

[black]
config = "build-support/pyproject.toml"

[isort]
config = ["build-support/pyproject.toml"]

[pylint]
config = "build-support/pylint.config"

[python-protobuf]
mypy_plugin = true

[mypy]
config = "build-support/pyproject.toml"
install_from_resolve = "mypy"
requirements = ["//3rdparty/python:mypy"]
EOF
```

### Test

```shell
pants tailor ::
pants test ::
```

**Output:**
```
Name                                              Stmts   Miss  Cover
---------------------------------------------------------------------
src/python/console-app/console_app/__init__.py        0      0   100%
src/python/console-app/console_app/util/util.py       3      0   100%
src/python/console-app/tests/__init__.py              0      0   100%
src/python/console-app/tests/util/util_test.py        5      0   100%
---------------------------------------------------------------------
TOTAL                                                 8      0   100%


Wrote xml coverage report to `dist/coverage/python`
```


Check if a report file is created.

```shell
ls dist/coverage/python
```
