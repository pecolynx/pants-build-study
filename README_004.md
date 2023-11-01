# pants-build-study

## 004. Fourth application

Create `old-app` using poetry.

```shell
cd src/python
poetry new old-app
cd old-app
python -m venv venv
. venv/bin/activate
pip install poetry
deactivate
. venv/bin/activate
poetry add pendulum=2.0.4
poetry install
deactivate
cd ../../../
```

### Write source codes

Write source code: `src/python/old-app/old_app/main.py`.

```python
cat <<EOF > src/python/old-app/old_app/main.py
from old_app.util.util import now

print('old-app')
x = now()
print(x)
EOF
```

Write source code: `src/python/old-app/old_app/util/util.py`.

```shell
mkdir -p src/python/old-app/old_app/util
```

```python
cat <<EOF > src/python/old-app/old_app/util/util.py
import pendulum

def now():
    return pendulum.now('Europe/Paris')
EOF
```


```shell
pants tailor ::
```

Update `src/python/old-app/old_app/util/BUILD` file.

```shell
cat <<EOF > src/python/old-app/old_app/util/BUILD
python_sources(
    dependencies=[
        "src/python/old-app:poetry#pendulum",
    ]
)
EOF
```

```shell
pants run src/python/old-app/old_app/main.py
```



```shell
cat <<EOF > src/python/old-app/BUILD
poetry_requirements(
    name="poetry",
)

python_sources(
    name="src",
    dependencies=[
        "src/python/old-app/old_app/**/*.py",
    ]
)

pex_binary(
    name="old-app",
    entry_point="old_app/main.py",
    dependencies=[
        ":src",
    ],
)
EOF
```


```shell
rm -rf dist
pants package ::
```

```shell
cd dist/src.python.old-app
unzip unzip old-app.pex
ls .deps
```

**Output:**
```
pendulum-2.0.4-cp311-cp311-manylinux_2_35_x86_64.whl
python_dateutil-2.8.2-py2.py3-none-any.whl
pytzdata-2020.1-py2.py3-none-any.whl
six-1.16.0-py2.py3-none-any.whl
```

```shell
cd ../../
```
