# Testing Framework for pisca-box

### Correctness

The containerised app does not necessarily run on a workstation.


### Before checkin
pytest
ruff --format=github --select=E9,F63,F7,F82 --target-version=py37 .
ruff --format=github --target-version=py37 .

### Github Actions
- ruff is used as a linter and the tests created in tests directory are run when a push is made to github
- Ruff can be installed from VSCode MarketPlace and will automatically execute contiunuously
  - The VSCode palette has Ruff: commands "quick fix" and "fix all" and "organize imports"
  - Ruff can be run from the command line too: https://pypi.org/project/ruff/0.0.105/ 
- Only succesful tests can be merged into main
- No pushes can be made directly to the main branch
- A reviewer is required to merge