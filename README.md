Odoo Release Manager
====================

With this module you would be able to create a initialised odoo database.
You would be able to configure any exists odoo database.

This odoo module populate a new shell command called `release`.

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

Goal
----

Our magic world is *automated deployment*. This is what we want to achive
with this odoo module.

Somehow we should be able to execute only one command against any database
then the command should apply automated release.

Proposal
--------

Create one folder (python package) for release steps. Every release step
should be an executable python script. All of these step should contain a 
`main` method.

When we execute `odoo release` command it should go through the available 
release steps and execute those steps which wasn't applied before.

Usage
-----

Put the `releases` folder path to odoo config like 
`releases=/usr/src/releases/`. This folder should be a python package itself.

Put a release step like `001_ensure_admin_technical_features.py`

    #!/usr/bin/python

    def main():
        Users = env["res.users"]
        admin = Users.browse(1)
        admin.write({"technical_features": True})

    if __name__ == "__main__":
        main()

Every steps will run only once against the same database.

Then execute `odoo-server release`.

Installation
------------

Make this addon available in Odoo. You don't have to install (you could).
First time when you execute the script it will install itself.

