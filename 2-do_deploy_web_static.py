#!/usr/bin/python3
"""
a Fabric script (based on the file 1-pack_web_static.py) that distributes an
archive to your web servers, using the function do_deploy
"""
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
    try:
        put(archive_path, "/tmp/{}".format(fName))

        run("rm -rf {}{}/".format(fDir, file))
        run("mkdir -p {}{}/".format(fDir, file))
        run("tar -xzf /tmp/{} -C {}{}/".format(fName, fDir, file))
        run("rm /tmp/{}".format(fName))
        run("mv /data/web_static/releases/{}/web_static/* "
                "/data/web_static/releases/{}/".format(file, file))
        run('rm -rf {}{}/web_static'.format(fDir, file))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(fDir, file))
        return True
    except Exception as e:
        print e
        return False
