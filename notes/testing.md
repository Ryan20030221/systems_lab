# Testing Notes

## assert
what assert does: tells you if there's a mismatch between your expected value and actual value

## Expected output
why a test needs a known correct answer:
or else you wouldn't know whether your code works or not

## Fake data
why fake data should be small:
because it shouldn't take that much time to test and create the data but also because the answer should be obvious

## Unit test
what a unit test checks:
it tests a specific function

## Regression test
what a regression test prevents:
prevents the error to come back again after changing the code

# GPU project connection
Why tests protect GPU analyzer conclusions:
it makes sure that all the functions did what it was supposed to and that there wasn't any
errors when say like parsing or filtering or validating and that all the valid data is actually valid data

## pytest
pytest is a test runner. Instead of manuall running every test file, I can run one command

python -m pytest

pytes discovers test files and test functions automatically if they follow naming rules.

a files hsould usually be named:

tests/test_name.py

a test function should start with:
def test_...

The main advantage is that future CI can run all tests automatically

## Temporary files

pytest can create temporary files/folders using the tmp_path fixture.

This is useful because file-reading tests can create their own fake files instead of depending on permanent project files.