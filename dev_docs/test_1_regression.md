
# Regression Testing

### In the development container (but not the app)
Run the regression tests from pytest and the lint formatting:
```
pytest
ruff --target-version=py37 --fix .
ruff --select=E9,F63,F7,F82 --target-version=py37 .
```

