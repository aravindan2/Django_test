# Django Tutorial

A Django project with a `polls` application.

[![Build Status](https://app.travis-ci.com/aravindan2/Django_test.svg?branch=master)](https://app.travis-ci.com/aravindan2/Django_test)
[![Coverage Status](https://coveralls.io/repos/github/aravindan2/Django_test/badge.svg?branch=master)](https://coveralls.io/github/aravindan2/Django_test?branch=master)

## Requirements

- Python 3.10 or later
- pip

## Local development

Install the project and its development/CI tools, apply database migrations, and
start the Django development server:

```shell
python -m venv .venv
# Activate the virtual environment before continuing.
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open <http://127.0.0.1:8000/> to view the application.

## Checks and tests

Run the same checks used by Travis CI:

```shell
black --check .
flake8 .
coverage run --source=polls manage.py test
```

The test command runs the Django test suite under Coverage.py. Travis uploads
the coverage report to Coveralls after a successful run.

## Travis CI and deployment

Travis CI runs the formatting, lint, and test checks on pushes and pull requests
for Python 3.10 through 3.14. Elastic Beanstalk deployment is limited to
successful builds from `master` and runs only once in the Python 3.14 job.
Travis does not deploy pull-request builds.

To enable deployment, configure these repository environment variables in
Travis CI:

- `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`: an AWS identity permitted to
  deploy to Elastic Beanstalk and access the deployment bucket.
- `AWS_BUCKET`: the Elastic Beanstalk application-version bucket in
  `us-east-1`.
- `COVERALLS_REPO_TOKEN`: the repository token used to publish coverage to
  Coveralls.

The deployment targets the `djangotutorial` Elastic Beanstalk application and
the `django-env` environment. Do not store AWS credentials or the Coveralls
token in the repository.