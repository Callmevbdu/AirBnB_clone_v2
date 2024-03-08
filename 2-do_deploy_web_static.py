#!/usr/bin/python3
"""
a Fabric script (based on the file 1-pack_web_static.py) that distributes an
archive to your web servers, using the function do_deploy
"""
from fabric.api import put, run, env
from os.path import exists

env.hosts = ['54.221.13.125', '52.91.117.179']


def do_deploy(archive_path):
    """
    Deploys the archive to web servers.
    """

    if not exists(archive_path):
        print(f"Archive not found: {archive_path}")
        return False
    try:
        fileName = archive_path.split("/")[-1]
        ext = fileName.split(".")[0]
        releasedir = "/data/web_static/releases/"
        put(archive_path, '/tmp/')

        run("mkdir -p {}{}/".format(releasedir, ext))
        run("tar -xzf /tmp/{} -C {}{}/".format(fileName, releasedir, ext))

        run("rm /tmp/{fileName}")
        run('mv {0}{1}/web_static/* {0}{1}/'.format(releasedir, ext))
        run('rm -rf {}{}/web_static'.format(releasedir, ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(releasedir, ext))
        return True
    except Exception as e:
        print(f"An error occurred during deployment: {e}")
        return False
