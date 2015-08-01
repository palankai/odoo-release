from __future__ import print_function

from contextlib import contextmanager

from openerp.api import Environment
from openerp.modules.registry import RegistryManager
from openerp.tools import config


def connectdb(dbname=None, uid=1, context=None):
    r = RegistryManager.get(dbname or config["db_name"])
    cr = r.cursor()
    Environment.reset()
    env = Environment(cr, uid, context or {})
    return env


@contextmanager
def odootx(dbname=None, uid=1, context=None):
    env = connectdb(dbname or config["db_name"], uid, context)
    try:
        yield env
        env.cr.commit()
    except:
        env.cr.rollback()
        raise

def install_addon(env, addon):
    module = env["ir.module.module"].search([("name", "=", addon)])
    if module.state != "installed":
        module.button_immediate_install()
    env.reset()
