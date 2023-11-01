poetry_requirements(
    name="poetry",
)

python_sources(
    name="src",
    dependencies=[
        "src/python/grpc-client/grpc_client/**/*.py",
    ]
)

pex_binary(
    name="grpc-client",
    entry_point="grpc_client/main.py",
    dependencies=[
        ":src",
    ],
)
