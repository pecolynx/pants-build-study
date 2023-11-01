# pants-build-study

## 001. First application

* Python 3.11.2
* Pants 2.17.0

Check python version.
```shell
python -V
```

**Output:**

```
Python 3.11.2
```

### Create a new directory


```shell
mkdir pants-build-study
cd pants-build-study
```

Write `.gitignore`.

```
cat <<EOF > .gitignore
venv
EOF
```

### Install `pants`

https://www.pantsbuild.org/docs/installation

```bash
curl --proto '=https' --tlsv1.2 -fsSL https://static.pantsbuild.org/setup/get-pants.sh | bash
```

### Create `console-app` using poetry

```shell
mkdir -p src/python
cd src/python
poetry new console-app
cd console-app
python -m venv venv
. venv/bin/activate
pip install poetry
deactivate
. venv/bin/activate
poetry add pendulum
poetry install
deactivate
```

### Write source codes

Write source code: `src/python/console-app/console_app/main.py`.

```python
cat <<EOF > console_app/main.py
from console_app.util.util import now

print('console-app')
x = now()
print(x)
EOF
```

Write source code: `src/python/console-app/console_app/util/util.py`.

```shell
mkdir -p console_app/util
```

```python
cat <<EOF > console_app/util/util.py
import pendulum

def now():
    return pendulum.now('Europe/Paris')
EOF
```

```
cd ../../../
```

### Create `pants.toml`

```toml
cat <<EOF > pants.toml
[GLOBAL]
pants_version = "2.17.0"

# https://www.pantsbuild.org/docs/enabling-backends
backend_packages = [
  "pants.backend.python",
]

[python]
interpreter_constraints = [">=3.11,<3.12"]

# https://www.pantsbuild.org/docs/source-roots
[source]
root_patterns = [
    "/src/python/*",
]
EOF
```

### Create `BUILD` files using `pants tailor` command

```shell
pants tailor ::
```

**Output:**
```
Created src/python/console-app/BUILD:
  - Add poetry_requirements target poetry
Created src/python/console-app/console_app/BUILD:
  - Add python_sources target console_app
Created src/python/console-app/console_app/util/BUILD:
  - Add python_sources target util
```

### Run application via source file

```shell
pants run src/python/console-app/console_app/main.py
```

**Output:**

```
console-app
2023-10-29T13:50:10.680589+01:00
```

### Run application via binary file

Add below `pex_binary` target to `src/python/console-app/BUILD`.

```
pex_binary(
    name="console-app",
    entry_point="console_app/main.py",
    dependencies=[
        ":src",
    ],
)
```


```shell
cat <<EOF > src/python/console-app/BUILD
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
EOF
```

Run application via binary file.

```shell
pants run src/python/console-app:console-app
```

`:console-app` in the above command is related to the name of `pex_binary` in `src/python/console-app/BUILD` file.
