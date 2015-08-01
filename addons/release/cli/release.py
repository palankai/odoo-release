from __future__ import print_function

import glob
import importlib
import os
import sys

import argparse
from openerp.cli import Command
from openerp.tools import config

from .. import odootx


class Release(Command):
    """Release based on release steps"""

    def run(self, args):
        parser = self.get_parser()
        options = parser.parse_args(args)
        env = odootx.connectdb(options.database)
        self.update_module_list(env)
        if self.ensure_installed(env):
            env = odootx.connectdb(options.database)

        applied = self.get_applied_steps(env)

        print("Execute upgrade steps...")
        path, steps = self.get_steps()
        sys.path.append(path)
        self.release_in_single_transaction(env, steps, exclude=applied)

    def get_parser(self):
        parser = argparse.ArgumentParser(
            prog="%s release" % sys.argv[0].split(os.path.sep)[-1],
            description=self.__doc__
        )
        parser.add_argument(
            '-d', dest="database", default=config["db_name"],
            help="database name (default=%s)" % config["db_name"]
        )
        return parser

    def update_module_list(self, env):
        env['ir.module.module'].update_list()

    def ensure_installed(self, env):
        module = env["ir.module.module"].search([("name", "=", "release")])
        if module.state != "installed":
            module.button_immediate_install()
            print("Release manager installed")
            return True
        return False

    def get_applied_steps(self, env):
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

    def release_in_single_transaction(self, env, steps, exclude):
        for name in steps:
            if not name in exclude:
                self.execute_step(env, name)

    def execute_step(self, env, name):
        mod = importlib.import_module(name)
        print("***** apply %s ******" % name)
        try:
            mod.main(env)
            self.store_applied(env, name)
            env.cr.commit()
        except:
            env.cr.rollback()
            raise

    def store_applied(self, env, name):
        Step = env["release.step"]
        Step.create({"name": name})
