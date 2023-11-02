# pants-build-study

## 005. Fifth application

Create `grpc-client` using poetry.

```shell
cd src/python
poetry new grpc-client
cd grpc-client
python -m venv venv
. venv/bin/activate
pip install poetry
deactivate
. venv/bin/activate
poetry add grpc-stubs
poetry install
deactivate
cd ../../../
```

### Write source codes

Write source code: `src/python/grpc-client/grpc_client/main.py`.

```python
cat <<EOF > src/python/grpc-client/grpc_client/main.py
import grpc
from helloworld.v1 import helloworld_pb2, helloworld_pb2_grpc


with grpc.insecure_channel("localhost:50052") as channel:
    stub = helloworld_pb2_grpc.GreeterStub(channel)
    response = stub.SayHello(helloworld_pb2.HelloRequest(name="John"))
print("Greeter client received: " + response.message)
EOF
```

```shell
pants tailor ::
```

```shell
cat <<EOF > src/python/grpc-client/BUILD
poetry_requirements(
    name="poetry",
)

pex_binary(
    name="grpc-client",
    entry_point="grpc_client/main.py",
)
EOF
```

```shell
rm -rf ./dist
pants package ::
```

Run gRPC server.

```shell
./dist/src.python.grpc-server/grpc-server.pex
```

Run gRPC client on another terminal.

```shell
./dist/src.python.grpc-client/grpc-client.pex
```

**Output:**
```
Greeter client received: Hello, John
```

