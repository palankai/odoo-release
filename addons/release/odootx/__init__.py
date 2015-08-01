from __future__ import print_function

from contextlib import contextmanager

import openerp
from openerp.api import Environment
from openerp.modules.registry import RegistryManager
from openerp.tools import config


def connectdb(dbname=None, uid=1, context=None):
    openerp.tools.config.parse_config([])
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
    finally:
        env.cr.close()

def install_addon(env, addon):
    module = env["ir.module.module"].search([("name", "=", addon)])
    if module.state != "installed":
        module.button_immediate_install()
    env.cr.commit()
    env.reset()

def set_xmlid(env, obj, name):
    ir_model_data = env['ir.model.data']
    ir_model_data.create({
        'model': obj._name,
        'res_id': obj.id,
        'module': '__export__',
        'name': name,
    })
