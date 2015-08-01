from __future__ import print_function

from openerp.modules.registry import RegistryManager
from openerp.api import Environment


def connectdb(dbname, uid=1, context=None):
    r = RegistryManager.get(dbname)
    cr = r.cursor()
    Environment.reset()
    env = Environment(cr, uid, context or {})
    return env
