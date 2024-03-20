poetry_requirements(
    name="poetry",
    resolve="grpc_client",
)

python_sources(
    name="src",
    sources=["grpc_client/**/*.py"],
    resolve="grpc_client",
)

pex_binary(
    name="grpc-client",
    resolve="grpc_client",
    entry_point="grpc_client/main.py",
)
