# Instructions for candidates

This is the Python version of the Payment Gateway challenge. If you haven't already read the [README.md](https://github.com/cko-recruitment) in the root of this organisation, please do so now. 

## Template structure
```
├── .editorconfig - don't change this. It ensures a consistent set of rules for submissions when reformatting code
├── .env.example
├── .python-version - Python version used by Pyenv (https://github.com/pyenv/pyenv).
├── Makefile - Makefile with commands such as install, run and test
├── docker-compose.yml - configures the bank simulator
├── pyproject.toml - project metadata, build system and dependencies
├── poetry.lock - Poetry lock file
├── main.py - app's entrypoint
├── payment_gateway_api/ - skeleton FastAPI API
├── imposters/ - contains the bank simulator configuration. Don't change this
└── tests/ - folder for tests
```

Feel free to change the structure of the solution, use a different test library etc.