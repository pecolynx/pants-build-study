poetry_requirements(
    name="poetry",
)

python_sources(
    name="grpc_client_3_09",
    sources=["grpc_client_3_09/**/*.py"],
    dependencies=[
        ":poetry",
    ],
)

pex_binary(
    name="grpc-client-3-09",
    interpreter_constraints=["CPython>=3.9,<3.10"],
    entry_point="grpc_client_3_09/main.py",
    dependencies=[
        ":grpc_client_3_09",
    ],
)
