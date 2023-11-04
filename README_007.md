# pants-build-study

## 007. Generating Source code from proto files for each resolve

### Add `grpc_client` resolve

Downgrade the grpcio version to use different resolve.

```
cd src/python/grpc-client
. venv/bin/activate
poetry add grpcio=1.58.0
poetry add protobuf
poetry install
deactivate
cd ../../..
```

Update `src/python/grpc-client/BUILD` file

```
cat <<EOF > src/python/grpc-client/BUILD
poetry_requirements(
    name="poetry",
    resolve="grpc_client",
)

pex_binary(
    name="grpc-client",
    resolve="grpc_client",
    entry_point="grpc_client/main.py",
)
EOF
```

### Add another `protobuf_sources` to BUILD file for proto files.

Add `protobuf_sources` to BUILD file for `grpc_client` resolve.

```
cat <<EOF > src/protos/helloworld/v1/BUILD
protobuf_sources(
    name="default",
    grpc=True,
)

protobuf_sources(
    name="grpc_client",
    grpc=True,
    python_resolve="grpc_client",
)
EOF
```

### Update BUILD files for grpc-client application

Update `src/python/grpc-client/grpc_client/BUILD` file.

```
cat <<EOF > src/python/grpc-client/grpc_client/BUILD
python_sources(
    resolve="grpc_client",
)
EOF
```

### Update pants.toml for grpc-client application

Add the below line to `pants.toml`

```
grpc_client = "3rdparty/python/grpc_client.lock"
```

```
cat <<EOF > pants.toml
[GLOBAL]
pants_version = "2.17.0"

backend_packages = [
    "pants.backend.python",
    "pants.backend.codegen.protobuf.python",
    "pants.backend.docker",
]

[python]
interpreter_constraints = [">=3.11,<3.12"]
enable_resolves = true
default_resolve = "default"

[python.resolves]
default = "3rdparty/python/default.lock"
old_app = "3rdparty/python/old_app.lock"
grpc_client = "3rdparty/python/grpc_client.lock"

[source]
root_patterns = [
    "/src/python/*",
    "/src/protos",
]
EOF
```

```
pants generate-lockfiles ::
```

Check if grpc-client runs properly.

```
pants run src/python/grpc-client/grpc_client/main.py
```

```
pants run src/python/grpc-client:grpc-client
```
