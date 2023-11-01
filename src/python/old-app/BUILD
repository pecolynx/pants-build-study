poetry_requirements(
    name="poetry",
    resolve="old_app",
)

python_sources(
    name="src",
    resolve="old_app",
    dependencies=[
        "src/python/old-app/old_app/**/*.py",
    ]
)

pex_binary(
    name="old-app",
    resolve="old_app",
    entry_point="old_app/main.py",
    dependencies=[
        ":src",
    ],
)
