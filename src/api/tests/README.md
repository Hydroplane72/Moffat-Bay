# Running the API Tests

## Requirements
- Python 3.9+
- `pytest` (install with `pip install pytest`)

## Run the tests
From the `SourceCode` folder:

```
python -m pytest api/tests -v
```

`conftest.py` adds `SourceCode` to `sys.path` so the tests can import `api.helpers` and `api.models` directly.

## Matt's notes
I do development in Visual Studio Code, so I am able to run the tests from within the IDE really easily. 