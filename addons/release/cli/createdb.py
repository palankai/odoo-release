from __future__ import print_function

import os
import sys

import argparse
from openerp.cli import Command
from openerp.service.db import DatabaseExists
from openerp.service.db import exp_create_database
from openerp.tools import config


class CreateDB(Command):
    """Create a new vanilla odoo database"""

    def run(self, args):
        parser = self.get_parser()
        options = parser.parse_args(args)

        try:
            exp_create_database(
                options.database, options.demo, options.lang, options.password
            )
            print("Database %s created." % options.database)
        except DatabaseExists:
            print("Database %s alredy exists" % options.database)


    def get_parser(self):
        parser = argparse.ArgumentParser(
            prog="%s createdb" % sys.argv[0].split(os.path.sep)[-1],
            description=self.__doc__
        )
        parser.add_argument(
            '-d', dest="database", default=config["db_name"],
            help="database name (default=%s)" % config["db_name"]
        )
        parser.add_argument(
            "--password", dest="password", default="admin",
            help="Password (default=admin)"
        )
        parser.add_argument(
            "--language", dest="lang", default="en_US",
            help="Language (default=en_US)"
        )
        parser.add_argument(
            "--load-demo", dest="demo", action="store_true", default=False,
            help="Load demo database"
        )
        return parser
