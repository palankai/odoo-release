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

    def main(env):
        Users = env["res.users"]
        admin = Users.browse(1)
        admin.write({"tz": "UTC"})

    if __name__ == "__main__":
        from odootx import odootx
        with odootx() as env:
            main()

Every steps will run only once against the same database.

Then execute `odoo-server release`.
You can still use `./001_admin_config.py` (if the python package installed)

**Important** calling the `release` is safe, never execute same script again
but you can call and execute any migration step directly any time.

Docker usage
------------

    docker run -d -e POSTGRES_USER=odoo -e POSTGRES_PASSWORD=odoo --name odoo_db postgres
    docker build -t myodoo .

    docker run --rm --link odoo_db:db myodoo -- release

Recomended directory structure and config
-----------------------------------------

    \Dockerfile
    \releases
        __init__.py
        0001_admin_config.py
    \addons
        release  # It should be just the addon itself
    \deploy
        openerp-sever.conf

Server config:

    [options]
    addons_path = /usr/lib/python2.7/dist-packages/openerp/addons,/usr/src/addons
    data_dir = /var/lib/odoo
    db_name = myodoo
    releases=/usr/src/releases

Minimal Dockerfile:

    FROM odoo:8
    ADD /usr/src/deploy/openerp-server.conf /etc/odoo/openerp-server.conf
    ADD . /usr/src/


Installation
------------

Make this addon available in Odoo. You don't have to install in odoo.
First time when you execute the script it will install itself.

### Execute step manually (optional)

If you want execute step directly from shell, you have to install the
python package part of this addon.
run `python setup.py install` to make sure odootx will be available.


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
