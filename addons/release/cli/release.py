from __future__ import print_function

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
        self.ensure_installed(env)

        print("Execute upgrade steps...")

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
        upgrader = env["ir.module.module"].search([("name", "=", "release")])
        if upgrader.state != "installed":
            upgrader.button_immediate_install()
            print("Release manager installed")
