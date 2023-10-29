poetry_requirements(
    name="poetry",
)

python_sources(
    name="src",
    dependencies=[
        "src/python/console-app/console_app/**/*.py",
    ]
)

pex_binary(
    name="console-app",
    entry_point="console_app/main.py",
    dependencies=[
        ":src",
    ],
)
