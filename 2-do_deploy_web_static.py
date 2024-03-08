#!/usr/bin/python3
# a Fabric script that distributes an archive to your web server
from fabric.api import put, run, env
import os.path

env.hosts = ['54.221.13.125', '52.91.117.179']


def do_deploy(archive_path):
    """
    Deploys the archive to web servers.
    """
    if os.path.isfile(archive_path) is False:
        return False
    fName = archive_path.split("/")[-1]
    file = fName.split(".")[0]
    fDir = "/data/web_static/releases/"
    current = "/data/web_static/current/"
    if put(archive_path, "/tmp/{}".format(fName)).failed is True:
        return False

    if run("rm -rf {}{}/".format(fDir, file)).failed is True:
        return False

    if run("mkdir -p {}{}/".format(fDir, file)).failed is True:
        return False

    if run("tar -xzf /tmp/{} -C {}{}/".
            format(fName, fDir, file)).failed is True:
        return False

    if run("rm /tmp/{}".format(fName)).failed is True:
        return False

    if run("mv {}{}/web_static/* {}{}/"
            .format(fDir, file, fDir, file)).failed is True:
        return False

    if run('rm -rf {}{}/web_static'.format(fDir, file)).failed is True:
        return False
    if run('rm -rf /data/web_static/current/').failed is True:
        return False

    if run('ln -s {}{}/ {}'.format(fDir, file, current)).failed is True:
        return False

    return True
