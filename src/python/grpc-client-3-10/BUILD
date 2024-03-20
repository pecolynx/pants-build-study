poetry_requirements(
    name="poetry",
    resolve="grpc_client_3_10",
)

python_sources(
    name="src",
    resolve="grpc_client_3_10",
    sources=["grpc_client_3_10/**/*.py"],
)

pex_binary(
    name="grpc-client-3-10",
    resolve="grpc_client_3_10",
    interpreter_constraints=["CPython>=3.10,<3.11"],
    entry_point="grpc_client_3_10/main.py",
)
