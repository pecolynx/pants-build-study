from console_app.util.util import now
import pendulum


def test_now():
    x = now()
    assert isinstance(x, pendulum.DateTime)






```
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

# [mypy-protobuf]
# # version = "mypy-protobuf==2.10"
# config = "build-support/pyproject.toml"
# # lockfile = "build-support/mypy_protobuf_lockfile.txt"

```

pants generate-lockfiles ::

pants tailor ::

pants test ::


https://www.pantsbuild.org/docs/reference-pytest

