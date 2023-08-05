# Contributing to midiroute

Thanks for deciding to contribute to this project! Please take some time to read this document before raising a PR.

## Contribution Workflow

* Raise an issue requesting a new feature (or reporting a defective one).
* Fork the repository.
* Raise a PR against our master branch with the proposed changes.
* Limit PRs to one change only.
* Always add tests for your code.
* Changes must pass the CI before they can be merged.
* We use a squash and merge flow when merging PRs.

## Code

* We use black with default settings to format our code. Our line length is 88 characters.
* We follow `pep-257` and `pep8` for code and docstrings.
* Docstrings follow the [google style](http://google.github.io/styleguide/pyguide.html#381-docstrings).

## Tests

* We use `pytest` to run our tests and write in the `pytest` style.
* No `unittest.TestCase` inheritance!
* Write `assert` statements in `expected == actual` style.
* Write descriptive test docstrings.
* You can run the test suite using `tox -e py37` or `tox -e py38` (or just `pytest` if you don't want to use `tox`).

## Local Development Environment

We recommend running the test suite using `tox`. However you can also run `pytest` directly after installing the package in `dev` mode.

Clone the `midiroute` repository

```
git clone git@github.com/rwalton00/midiroute.git && cd midiroute
```

To set up a traditional dev environment, first create a virtual environment

```
python -m venv .midiroute-env
```

Then activate your virtual environment

```
source .midiroute-env/bin/activate
```

Install an editable version of `midiroute` along with the dev dependencies

```
$ pip install -e '.[dev]'
$ pre-commit install
```
The `pre-commit` hooks will run on each commit and ensure you don't push code that violates our style guide.

Running the tests should now work and the tests should pass

```
python -m pytest
```

Have fun!
