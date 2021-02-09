#!/usr/bin/env python

import os
import sys

# set the Django root folder here
APP_DIR = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "django_rapyd_wiretap"
)
sys.path.insert(0, APP_DIR)

# specify the django settings module
os.environ["DJANGO_SETTINGS_MODULE"] = "django_rapyd_wiretap.settings"


def main():
    # initialize django
    import django

    django.setup()

    # instantiate test runner
    from django.conf import settings
    from django.test.utils import get_runner

    TestRunner = get_runner(settings)

    # and then run tests and return the results
    test_runner = TestRunner(verbosity=1, interactive=False)
    failures = test_runner.run_tests(["wiretap"])
    sys.exit(bool(failures))


if __name__ == "__main__":
    main()
