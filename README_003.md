# pants-build-study

## 003. Third application

Create another application that uses `pendulum`.

### Check dependencies of `console-app`

```shell
pants peek src/python/console-app/console_app/util/util.py
```

**Output:**
```
[
  {
    "address": "src/python/console-app/console_app/util/util.py",
    "target_type": "python_source",
    "dependencies": [
      "src/python/console-app:poetry#pendulum"
    ],
```

You can see that `console-app` depends on `src/python/console-app:poetry#pendulum`.

### Create `console2-app` using poetry

```shell
cd src/python
poetry new console2-app
cd console2-app
python -m venv venv
. venv/bin/activate
pip install poetry
deactivate
. venv/bin/activate
poetry add pendulum
poetry install
deactivate
cd ../../../
```

### Write source codes

Write source code: `src/python/console2-app/console2_app/main.py`.

```python
cat <<EOF > src/python/console2-app/console2_app/main.py
from console2_app.util.util import now

print('console2-app')
x = now()
print(x)
EOF
```

Write source code: `src/python/console2-app/console2_app/util/util.py`.

```shell
mkdir -p src/python/console2-app/console2_app/util
```

```python
cat <<EOF > src/python/console2-app/console2_app/util/util.py
import pendulum

def now():
    return pendulum.now('Europe/Paris')
EOF
```


```shell
pants tailor ::
```

### Run application

```shell
pants run src/python/console-app/console_app/main.py
```

**Output:**

```
Traceback (most recent call last):
  File "/tmp/pants-sandbox-n8l3my/./.cache/pex_root/venvs/4cc0b1a06847eddb3e2b2fca231d89d1240f8d9d/dd50d8563c27f406491b760155d53072745cd67f/pex", line 274, in <module>
    runpy.run_module(module_name, run_name="__main__", alter_sys=True)
  File "<frozen runpy>", line 226, in run_module
  File "<frozen runpy>", line 98, in _run_module_code
  File "<frozen runpy>", line 88, in _run_code
  File "/tmp/pants-sandbox-n8l3my/src/python/console-app/console_app/main.py", line 1, in <module>
    from console_app.util.util import now
  File "/tmp/pants-sandbox-n8l3my/src/python/console-app/console_app/util/util.py", line 1, in <module>
    import pendulum
ModuleNotFoundError: No module named 'pendulum'
```

Why did you get the above error?


### Check dependencies of `console-app` again

```shell
pants peek src/python/console-app/console_app/util/util.py
```

You can see that dependencies are missing.

**Output:**
```
[
  {
    "address": "src/python/console-app/console_app/util/util.py",
    "target_type": "python_source",
    "dependencies": [],
```

To fix this issue, update `src/python/console-app/console_app/util/BUILD` file.

```shell
cat <<EOF > src/python/console-app/console_app/util/BUILD
python_sources(
    dependencies=[
        "src/python/console-app:poetry#pendulum",
    ]
)
EOF
```

Also update `src/python/console2-app/console2_app/util/BUILD` file.

```shell
cat <<EOF > src/python/console2-app/console2_app/util/BUILD
python_sources(
    dependencies=[
        "src/python/console2-app:poetry#pendulum",
    ]
)
EOF
```

### Run application again

```shell
pants run src/python/console-app/console_app/main.py
```

**Output:**

```
console-app
2023-10-30T16:40:33.634042+01:00
```

Succeeded!
