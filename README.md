# Password hashing - API tests 

Tests for broken-hashserve code.

# System pre-requisites 
Your Mac should have created an environment and have installed:
- pip3 
- python3

# Setting up 

- Activate the environment
> pipenv shell

- Installing packages
> pipenv install requests

- Installing pytest
> pip3 install pytest 

# Running tests

Running tests from the command line can be done with the following:

- Run tests in a module:
> pytest test_mod.py

- Run a specific test within a module:
> pytest test_mod.py::test_func