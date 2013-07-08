#!/usr/bin/env python

# http://ericholscher.com/blog/2009/jun/29/enable-setuppy-test-your-django-apps/
# http://www.travisswicegood.com/2010/01/17/django-virtualenv-pip-and-fabric/
# http://code.djangoproject.com/svn/django/trunk/tests/runtests.py
# https://github.com/tomchristie/django-rest-framework/blob/master/rest_framework/runtests/runtests.py
import os
import sys

# fix sys path so we don't need to setup PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
os.environ['DJANGO_SETTINGS_MODULE'] = 'djmx.runtests.settings'
if len(sys.argv) == 2:
    os.environ['DATABASE_ENGINE'] = sys.argv[1]

from django.conf import settings
from django.test.utils import get_runner


if __name__ == '__main__':
    runner = get_runner(settings)
    if getattr(runner, 'func_name', None) == 'run_tests':
        # Django 1.1
        sys.exit(runner(['djmx']))
    sys.exit(runner().run_tests(['djmx']))
