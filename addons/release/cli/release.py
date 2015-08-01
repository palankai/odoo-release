from __future__ import print_function

import glob
import importlib
import os
import sys

import argparse
import openerp
from openerp.cli import Command
from openerp.service import db, server
from openerp.tools import config

from .. import odootx


class Release(Command):
    """Release based on release steps"""

    def run(self, args):
        openerp.tools.config.parse_config(args)
        openerp.cli.server.report_configuration()
        server.start(preload=[], stop=True)
        self.ensure_database()
        self.install_release_manager()
        applied = self.get_applied_steps()
        path, steps = self.get_steps()
        if steps:
            sys.path.append(path)
            self.release(steps, exclude=applied)

    def get_parser(self):
        parser = argparse.ArgumentParser(
            prog="%s release" % sys.argv[0].split(os.path.sep)[-1],
            description=self.__doc__
        )
        return parser

    def ensure_database(self):
        try:
            db._create_empty_database(config["db_name"])
        except db.DatabaseExists:
            pass

    def install_release_manager(self):
        with odootx.odootx() as env:
            env['ir.module.module'].update_list()
            module = env["ir.module.module"].search(
                [("name", "=", "release")]
            )
            if module.state != "installed":
                module.button_immediate_install()

    def get_applied_steps(self):
        with odootx.odootx() as env:
            Step = env["release.step"]
            return [step.name for step in Step.search([])]


    def get_steps(self):
        path = self._get_steps_path()
        steps = []
        for filepath in glob.glob(os.path.join(path, "*.py")):
            fn = os.path.basename(filepath)
            if fn != "__init__.py":
                mod, _ = os.path.splitext(fn)
                steps.append(mod)
        return path, sorted(steps)

    def _get_steps_path(self):
        path = config.get("releases", None)
        if not path:
            print(
                "Setup 'releases' in config file, it should be"
                " the absoulte path of release steps directory"
            )
            sys.exit(1)
        return path

    def release(self, steps, exclude):
        for name in steps:
            if not name in exclude:
                self.execute_step(name)

    def execute_step(self, name, store=True):
        mod = importlib.import_module(name)
        print("***** apply %s ******" % name)
        with odootx.odootx(config["db_name"]) as env:
            mod.main(env)
            if store:
                self.store_applied(env, name)

    def store_applied(self, env, name):
        Step = env["release.step"]
        Step.create({"name": name})
