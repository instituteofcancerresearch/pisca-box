
# Regression Testing

### In the development container (but not the app)
Run the regression tests from pytests and the lint formatting:
```
pytest
ruff --format=github --select=E9,F63,F7,F82 --target-version=py37 .
ruff --format=github --target-version=py37 .
```

