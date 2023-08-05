# Example python package

example how to create python package and deploy to pip registory

## Prerequisite

- install wheel

```python
python3 -m pip install --user --upgrade setuptools wheel
```

- intstall twine

```python
python3 -m pip install --user --upgrade twine
```

## Build & Deploy Steps

- Go to setup.py directories and run the following command
  - it will generated a lot of files include *dist* directory which include package

```python
python3 setup.py sdist bdist_wheel
```

- 