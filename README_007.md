# pants-build-study

## 007. 

```
cd src/python/grpc-client
. venv/bin/activate
poetry add grpcio=1.58.0
poetry add protobuf
poetry install
deactivate
cd ../../..
```


```
poetry_requirements(
    name="poetry",
    resolve="grpc_client",
)

python_sources(
    name="src",
    resolve="grpc_client",
    dependencies=[
        "src/python/grpc-client/grpc_client/**/*.py",
    ]
)

pex_binary(
    name="grpc-client",
    resolve="grpc_client",
    entry_point="grpc_client/main.py",
    dependencies=[
        ":src",
    ],
)

```

src/protos/helloworld/v1/BUILD

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

```
python_sources(
    resolve="grpc_client",
)
```

```
pants run src/python/grpc-client/grpc_client/main.py
```

```
pants run src/python/grpc-client:grpc-client
```
