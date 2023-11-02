# pants-build-study

## 008. Linters and formatters

https://www.pantsbuild.org/docs/python-linters-and-formatters



Add `"pants.backend.python.lint.bandit",` to `backend_packages` in `GLOBAL` seciton.


Apply linter.

```
pants lint ::
```

Format codes.

```
pants fmt ::
```

```shell
mkdir build-support
```

```
[MASTER]
disable=
    C0114, # missing-module-docstring
    C0115, # missing-class-docstring
    C0116, # missing-function-docstring
    E1101, # no-member

```


build-support/pyproject.toml

```toml
[tool.isort]
profile = "black"
line_length = 100

[tool.black]
line-length = 100
```

https://www.pantsbuild.org/docs/python-check-goal

```
"pants.backend.python.typecheck.mypy",
```


```toml
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

[mypy]
config = "build-support/pyproject.toml"
install_from_resolve = "mypy"
requirements = ["//3rdparty/python:mypy"]


```



3rdparty/python/mypy-requirements.txt

```
mypy==1.1.1
mypy-extensions==1.0.0
typing_extensions==4.8.0
```


3rdparty/python/BUILD
```
cat <<EOF > 3rdparty/python/BUILD
python_requirements(
    name="mypy",
    source="mypy-requirements.txt",
    resolve="mypy",
)
EOF
```

```shell
pants generate-lockfiles ::
```

[python-protobuf]
mypy_plugin = true

```
pants export-codegen ::
```

```
pants check ::
```
