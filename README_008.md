# pants-build-study

## 008. Linters and formatters

https://www.pantsbuild.org/docs/python-linters-and-formatters

### Add bandit

Add `"pants.backend.python.lint.bandit",` to `backend_packages` in `GLOBAL` seciton.

```toml
cat <<EOF >pants.toml
[GLOBAL]
pants_version = "2.17.0"

backend_packages = [
    "pants.backend.python",
    "pants.backend.python.lint.bandit",
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
EOF
```

Apply linter.

```
pants lint ::
```

### Add other linters

```shell
mkdir build-support
```

Add config file for pylint.

```
cat <<EOF >build-support/pylint.config
[MASTER]
disable=
    C0114, # missing-module-docstring
    C0115, # missing-class-docstring
    C0116, # missing-function-docstring
    E1101, # no-member
    R0903, # too-few-public-methods
EOF
```

Add config file for isort and black.



```toml
cat <<EOF >build-support/pyproject.toml
[tool.isort]
profile = "black"
line_length = 100

[tool.black]
line-length = 100
EOF
```

Add below lines to `backend_packages` in `GLOBAL` seciton in `pants.toml` file.

```
"pants.backend.python.lint.bandit",
"pants.backend.python.lint.black",
"pants.backend.python.lint.docformatter",
"pants.backend.docker.lint.hadolint",
"pants.backend.python.lint.isort",
"pants.backend.python.lint.pylint",
"pants.backend.python.lint.pyupgrade",
"pants.backend.experimental.python.lint.ruff",
```

```toml
cat <<EOF >pants.toml
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
EOF
```

Format codes.

https://www.pantsbuild.org/docs/reference-fmt

```
pants fmt ::
```


Apply linter.

https://www.pantsbuild.org/docs/reference-lint

```
pants lint ::
```

### Add mypy

https://www.pantsbuild.org/docs/python-check-goal

```
"pants.backend.python.typecheck.mypy",
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
old_app = "3rdparty/python/old_app.lock"
grpc_client = "3rdparty/python/grpc_client.lock"

[source]
root_patterns = [
    "/src/python/*",
    "/src/protos",
]

[python-protobuf]
mypy_plugin = true


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
EOF
```

Write requirements.txt for mypy.


```
cat <<EOF >3rdparty/python/mypy-requirements.txt
mypy==1.6.1
mypy-extensions==1.0.0
tomli==2.0.1
typing_extensions==4.8.0
EOF
```

Write BUILD fild for mypy.

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

Generate source files from proto files.

```
pants export-codegen ::
```

Check if *.pyi files are generated.

```
ls dist/codegen/src/protos/helloworld/v1/
```

Check mypy.

```
pants check ::
```

**Output:**

```
Partition #1 - default, ['CPython<3.12,>=3.11']:
src/protos/helloworld/v1/helloworld_pb2.pyi:19: error: Library stubs not installed for "google.protobuf.descriptor"  [import-untyped]
src/protos/helloworld/v1/helloworld_pb2.pyi:19: note: Hint: "python3 -m pip install types-protobuf"
src/protos/helloworld/v1/helloworld_pb2.pyi:19: note: (or run "mypy --install-types" to install all missing stub packages)
src/protos/helloworld/v1/helloworld_pb2.pyi:19: error: Library stubs not installed for "google.protobuf"  [import-untyped]
src/protos/helloworld/v1/helloworld_pb2.pyi:19: error: Skipping analyzing "google": module is installed, but missing library stubs or py.typed marker  [import-untyped]
src/protos/helloworld/v1/helloworld_pb2.pyi:20: error: Library stubs not installed for "google.protobuf.message"  [import-untyped]
src/protos/helloworld/v1/helloworld_pb2_grpc.pyi:19: error: Skipping analyzing "grpc": module is installed, but missing library stubs or py.typed marker  [import-untyped]
src/python/grpc-server/grpc_server/main.py:3: error: Skipping analyzing "grpc": module is installed, but missing library stubs or py.typed marker  [import-untyped]
src/python/grpc-server/grpc_server/main.py:3: note: See https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-imports
Found 6 errors in 3 files (checked 8 source files)

Partition #2 - grpc_client, ['CPython<3.12,>=3.11']:
src/protos/helloworld/v1/helloworld_pb2.pyi:19: error: Library stubs not installed for "google.protobuf.descriptor"  [import-untyped]
src/protos/helloworld/v1/helloworld_pb2.pyi:19: note: Hint: "python3 -m pip install types-protobuf"
src/protos/helloworld/v1/helloworld_pb2.pyi:19: note: (or run "mypy --install-types" to install all missing stub packages)
src/protos/helloworld/v1/helloworld_pb2.pyi:19: note: See https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-imports
src/protos/helloworld/v1/helloworld_pb2.pyi:19: error: Library stubs not installed for "google.protobuf"  [import-untyped]
src/protos/helloworld/v1/helloworld_pb2.pyi:19: error: Skipping analyzing "google": module is installed, but missing library stubs or py.typed marker  [import-untyped]
src/protos/helloworld/v1/helloworld_pb2.pyi:20: error: Library stubs not installed for "google.protobuf.message"  [import-untyped]
Found 4 errors in 1 file (checked 2 source files)

Partition #3 - old_app, ['CPython<3.12,>=3.11']:
src/python/old-app/old_app/util/util.py:1: error: Skipping analyzing "pendulum": module is installed, but missing library stubs or py.typed marker  [import-untyped]
src/python/old-app/old_app/util/util.py:1: note: See https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-imports
Found 1 error in 1 file (checked 3 source files)
```

Some errors occurred.

Currently, the purpose is not to fix the source code. Ignore these errors.

Update `build-support/pyproject.toml` config file.
```
cat <<EOF > build-support/pyproject.toml
[tool.isort]
profile = "black"
line_length = 100

[tool.black]
line-length = 100

[tool.mypy]
ignore_missing_imports = true

[[tool.mypy.overrides]]
module = ['helloworld.v1.*']
ignore_errors = true
EOF
```

Check mypy again.

```
pants check ::
```

```
19:06:00.61 [INFO] Completed: Typecheck using MyPy - mypy - mypy succeeded.
Partition #1 - default, ['CPython<3.12,>=3.11']:
Success: no issues found in 8 source files

Partition #2 - grpc_client, ['CPython<3.12,>=3.11']:
Success: no issues found in 2 source files

Partition #3 - old_app, ['CPython<3.12,>=3.11']:
Success: no issues found in 3 source files
```

Passed!
