# pants-build-study

## 002. Second application

Create `grpc-server` using poetry.

```shell
cd src/python
poetry new grpc-server
cd grpc-server
python -m venv venv
. venv/bin/activate
pip install poetry
deactivate
. venv/bin/activate
poetry add grpcio
poetry add protobuf
poetry install
deactivate
cd ../../../
```

Create proto file.

```proto
mkdir -p src/protos/helloworld/v1
cat <<EOF > src/protos/helloworld/v1/helloworld.proto
// Copyright 2015 gRPC authors.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

syntax = "proto3";

package helloworld.v1;

option java_multiple_files = true;
option java_outer_classname = "HelloWorldProto";
option java_package = "io.grpc.examples.helloworld";
option objc_class_prefix = "HLW";

// The greeting service definition.
service Greeter {
  // Sends a greeting
  rpc SayHello(HelloRequest) returns (HelloReply) {}

  rpc SayHelloStreamReply(HelloRequest) returns (stream HelloReply) {}

  rpc SayHelloBidiStream(stream HelloRequest) returns (stream HelloReply) {}
}

// The request message containing the user's name.
message HelloRequest {
  string name = 1;
}

// The response message containing the greetings
message HelloReply {
  string message = 1;
}
EOF
```

Add `"pants.backend.codegen.protobuf.python",` to `backend_packages` in `GLOBAL` section.

Add `"/src/protos",` to `root_patterns` in `source` section.

```toml
cat <<EOF > pants.toml
[GLOBAL]
pants_version = "2.17.0"

backend_packages = [
    "pants.backend.python",
    "pants.backend.codegen.protobuf.python",
]

[python]
interpreter_constraints = [">=3.11,<3.12"]

[source]
root_patterns = [
    "/src/python/*",
    "/src/protos",
]
EOF
```

Create `BUILD` files using `pants tailor` command.

```
pants tailor ::
```

**Output:**
```
Created src/protos/helloworld/v1/BUILD:
  - Add protobuf_sources target v1
Created src/python/grpc-server/BUILD:
  - Add poetry_requirements target poetry
```


Update `BUILD` file.

```shell
cat <<EOF > src/protos/helloworld/v1/BUILD
protobuf_sources(
    grpc=True,
)
EOF
```

```python
cat <<EOF >  src/python/grpc-server/grpc_server/main.py
from helloworld.v1.helloworld_pb2_grpc import GreeterServicer

print(GreeterServicer())
EOF
```

Create `BUILD` files using `pants tailor` command.

```shell
pants tailor ::
```

Test application.

```shell
pants run src/python/grpc-server/grpc_server/main.py
```

**Output:**
```
<helloworld.v1.helloworld_pb2_grpc.GreeterServicer object at 0x7fd0a35057d0>
```


```python
cat <<EOF > src/python/grpc-server/grpc_server/main.py
from concurrent import futures

import grpc
from helloworld.v1 import helloworld_pb2, helloworld_pb2_grpc


class GreeterServicer(helloworld_pb2_grpc.GreeterServicer):
    def SayHello(self, request: helloworld_pb2.HelloRequest, context: grpc.ServicerContext) -> helloworld_pb2.HelloReply:
        return helloworld_pb2.HelloReply(message=f"Hello, {request.name}")


server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
helloworld_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)
server.add_insecure_port(f"[::]:50052")
server.start()
print('gRPC server listening at :50052')
server.wait_for_termination()
EOF
```

```shell
pants run src/python/grpc-server/grpc_server/main.py
```

**Output:**
```
gRPC server listening at :50052
```

Exec `Ctrl+C` command to stop the server application.


Update `BUILD` file: `src/python/grpc-server/BUILD`.


```shell
cat <<EOF > src/python/grpc-server/BUILD
poetry_requirements(
    name="poetry",
)

python_sources(
    name="src",
    dependencies=[
        "src/python/grpc-server/grpc_server/**/*.py",
    ]
)

pex_binary(
    name="grpc-server",
    entry_point="grpc_server/main.py",
    dependencies=[
        ":src",
    ],
)
EOF
```


```shell
rm -rf dist
```

```shell
pants package ::
```

**Output:**

```
00:35:43.16 [INFO] Wrote dist/src.python.console-app/console-app.pex
00:35:43.16 [INFO] Wrote dist/src.python.grpc-server/grpc-server.pex

```

Check whether a pex file is created.

```shell
ls dist/src.python.grpc-server/grpc-server.pex
```

Write Docker file.

```dockerfile
cat <<EOF > src/python/grpc-server/Dockerfile
FROM python:3.11.2-slim-buster

WORKDIR /opt/app

COPY src.python.grpc-server/grpc-server.pex /opt/app/grpc_server.pex

ENTRYPOINT ["/bin/bash", "-c", "/opt/app/grpc_server.pex"]
EOF
```

Add `"pants.backend.docker",` to `pants.toml`.

```toml
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

[source]
root_patterns = [
    "/src/python/*",
    "/src/protos",
]
EOF
```


Add below `docker_image` target to `src/python/grpc-server/BUILD`.

```
docker_image(
    name="docker",
    repository="grpc-server",
)
```

```shell
cat <<EOF > src/python/grpc-server/BUILD
poetry_requirements(
    name="poetry",
)

python_sources(
    name="src",
    dependencies=[
        "src/python/grpc-server/grpc_server/**/*.py",
    ]
)

pex_binary(
    name="grpc-server",
    entry_point="grpc_server/main.py",
    dependencies=[
        ":src",
    ],
)

docker_image(
    name="docker",
    repository="grpc-server",
)
EOF
```

Build a docker image.

```shell
pants package ::
```

Check whether an image is created.

```shell
docker images
```

**Output:**
```
REPOSITORY     TAG       IMAGE ID       CREATED         SIZE
grpc-server    latest    5175e22508ed   4 minutes ago   127MB
```
