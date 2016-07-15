from . import BaseReport
from flask import current_app
import importlib
import inspect
import traceback

def get_report(module, report):
    try:
        module = importlib.import_module("modules.{}.reports".format(module))
        c = getattr(module, report)
        if inspect.isclass(c) and issubclass(c, BaseReport):
            return c()
        return None
    except:
        return None

def get_reports(module):
    try:
        module = importlib.import_module("modules.{}.reports".format(module))
        members = [i[1] for i in inspect.getmembers(module)]
        reports = [i for i in members if
                    inspect.isclass(i) and
                    issubclass(i, BaseReport) and
                    i is not BaseReport]

        return sorted(reports, key=lambda k: k.name)
    except ImportError:
        return []

def get_all_reports():
    data = [(i, get_reports(i)) for i in sorted(current_app.blueprints.keys())]
    return [i for i in data if i[1]]
