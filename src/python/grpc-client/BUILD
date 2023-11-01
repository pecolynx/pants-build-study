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
