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
