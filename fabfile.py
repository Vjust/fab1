from __future__ import with_statement
from fabric.api import local, settings, abort, run, cd, env
from fabric.contrib.console import confirm
from fabvenv import virtualenv

env.use_ssh_config = True
env.hosts = ["sjac-dev1"]


def test():
    local("./manage.py test myapp")


def commit():
    with settings(warn_only=True):
        result = local("git add . && git commit -m 'checkedin'", capture=True)
    if result.failed and not confirm("Git failed. Continue?"):
        abort("Aborting per user request")


def push():
    local("git push")


def prepare_deploy():
    test()
    commit()
    push()


def deploy():
    code_dir = "/home/vjust/django/myproject"
    with settings(warn_only=True):
        # first time
        if run("test -d %s" % code_dir).failed:
            run("git clone git@github.com:syriajustice/fab1 %s" % code_dir)
            with cd(code_dir):
                run("virtualenv env")
                run("source env/bin/activate")
    with cd(code_dir):
        run("pwd")
        run("git pull")
        run("touch app.wsgi")
        with virtualenv(code_dir + "/env"):
            run("pwd")
            run("type python")
            run("./manage.py migrate")
            run("./manage.py runserver 8001")
