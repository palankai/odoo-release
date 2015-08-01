Odoo Release Manager
====================

With this module you would be able to create an initialised odoo database.
You would be able to configure any exists odoo database step-by-step with
only one command.

This odoo module populate a new cli command called `release`.

Usage
-----

Put the `releases` folder path to odoo config like 
`releases=/usr/src/releases/`. This folder should be a python package itself.

Put a release step like `001_admin_config.py`

    #!/usr/bin/python

    from odootx import odootx


    def main():
        with odootx() as env:
            Users = env["res.users"]
            admin = Users.browse(1)
            admin.write({"tz": "UTC"})

    if __name__ == "__main__":
        main()

Every steps will run only once against the same database.

Then execute `odoo-server release`.
You can still use `./001_admin_config.py`

**Important** calling the `release` is safe, never execute same script again
but you can call and execute any migration step directly any time.

Installation
------------

Make this addon available in Odoo. You don't have to install (you could).
First time when you execute the script it will install itself.


Background
----------

As an Odoo module developer it's very painful when (part of a team) I have to
release to production server. There are lots of manual steps. Workaround 
is we've created a release note what we update before every release.
This contains manual steps what we have to follow during the release.
Even if it's tested (we usually try it before) still manual.
Steps could be install or upgrade module, execute SQL scripts, execute
Odoo methods through XMLRPC.
Our avarage release takes 1-2 hours, and still risky to misread or just miss
a step. Other main issue is very difficult to run tests on our CI server.
We have to apply the release there as well.
