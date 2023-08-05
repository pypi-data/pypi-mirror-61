# -*- coding: utf-8 -*-
import os
import re
import six
import django
import pytest
import inspect

from django.core.management import call_command
from django.db.models import Model
from django.test import override_settings

from django_extensions.management.commands import shell_plus
from django_extensions.management.shells import SHELL_PLUS_DJANGO_IMPORTS


@pytest.mark.skipif(django.VERSION < (2, 0), reason="This test works only on Django greater than 2.0.0")
@pytest.mark.django_db()
@override_settings(SHELL_PLUS_SQLPARSE_ENABLED=False, SHELL_PLUS_PYGMENTS_ENABLED=False)
def test_shell_plus_print_sql(capsys):
    out = six.StringIO()
    try:
        from django.db import connection
        from django.db.backends import utils
        CursorDebugWrapper = utils.CursorDebugWrapper
        force_debug_cursor = True if connection.force_debug_cursor else False
        call_command("shell_plus", plain=True, print_sql=True, command="User.objects.all().exists()")
    finally:
        utils.CursorDebugWrapper = CursorDebugWrapper
        connection.force_debug_cursor = force_debug_cursor

    out, err = capsys.readouterr()

    assert re.search(r"SELECT\s+.+\s+FROM\s+.auth_user.\s+LIMIT\s+1", out)


def test_shell_plus_plain_startup():
    parser = shell_plus.Command().create_parser("test", "shell_plus")
    args = ["--plain"]
    options = parser.parse_args(args=args)

    command = shell_plus.Command()
    command.tests_mode = True
    retcode = command.handle(**vars(options))

    assert retcode == 130


def test_shell_plus_plain_startup_with_pythonrc(monkeypatch):
    parser = shell_plus.Command().create_parser("test", "shell_plus")
    args = ["--plain", "--use-pythonrc"]
    options = parser.parse_args(args=args)

    tests_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    pythonrc_file = os.path.join(tests_dir, 'pythonrc.py')
    assert os.path.isfile(pythonrc_file)
    monkeypatch.setenv('PYTHONSTARTUP', pythonrc_file)

    command = shell_plus.Command()
    command.tests_mode = True

    retcode = command.handle(**vars(options))
    assert retcode == 130

    imported_objects = command.tests_imported_objects
    assert 'pythonrc_test_func' in imported_objects
    assert imported_objects['pythonrc_test_func']() == "pythonrc was loaded"


def test_shell_plus_plain_loading_standard_django_imports(monkeypatch):
    parser = shell_plus.Command().create_parser("test", "shell_plus")
    args = ["--plain"]
    options = parser.parse_args(args=args)

    command = shell_plus.Command()
    command.tests_mode = True

    retcode = command.handle(**vars(options))
    assert retcode == 130

    imported_objects = command.tests_imported_objects
    assert 'get_user_model' in imported_objects
    assert 'settings' in imported_objects
    assert 'timezone' in imported_objects


def test_shell_plus_plain_loading_django_extensions_modules(monkeypatch):
    parser = shell_plus.Command().create_parser("test", "shell_plus")
    args = ["--plain"]
    options = parser.parse_args(args=args)

    command = shell_plus.Command()
    command.tests_mode = True

    retcode = command.handle(**vars(options))
    assert retcode == 130

    imported_objects = command.tests_imported_objects
    assert 'Club' in imported_objects
    assert 'UniqueTestAppModel' in imported_objects
    assert 'RandomCharTestModel' in imported_objects


def test_shell_plus_get_imported_objects():
    command = shell_plus.Command()
    objs = command.get_imported_objects({})
    for items in SHELL_PLUS_DJANGO_IMPORTS.values():
        for item in items:
            assert item in objs, "%s not loaded by get_imported_objects()" % item


def assert_should_models_be_imported(should_be, cli_arguments=None):
    command = shell_plus.Command()
    objs = command.get_imported_objects(cli_arguments or {})
    imported_models = filter(lambda imported: inspect.isclass(imported) and issubclass(imported, Model), objs.values())
    assert bool(list(imported_models)) == should_be


def test_shell_plus_loading_models():
    assert_should_models_be_imported(True)


def test_shell_plus_skipping_models_import_cli():
    assert_should_models_be_imported(False, cli_arguments={'dont_load': ['*']})


@override_settings(SHELL_PLUS_DONT_LOAD=['*'])
def test_shell_plus_skipping_models_import_settings():
    assert_should_models_be_imported(False)
