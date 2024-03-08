#!/usr/bin/python3
"""
 Fabric script that creates and distributes an archive to your web servers,
 using the function deploy.
"""
import os.path
from datetime import datetime
from fabric.api import env, local, put, run

env.hosts = ["54.221.13.125", "52.91.117.179"]


def do_pack():
    """
    Compresses the web_static folder into a .tgz archive.
    """

    now = datetime.now()
    form = 'web_static_' + now.strftime("%Y%m%d%H%M%S") + '.' + 'tgz'

    local('mkdir -p versions')

    tgz = local("tar -czvf versions/{} web_static/".format(form))

    if tgz is not None:
        return form
    else:
        return None


def do_deploy(archive_path):

    """Distributes an archive to a web server.

    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        Error occurs - False.
        Otherwise - True.
    """
    if os.path.isfile(archive_path) is False:
        return False
    fName = archive_path.split("/")[-1]
    file = fName.split(".")[0]
    fDir = "/data/web_static/releases/"
    current = "/data/web_static/current"
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

    if run('rm -rf /data/web_static/current').failed is True:
        return False

    if run('ln -s {}{}/ {}'.format(fDir, file, current)).failed is True:
        return False

    return True


def deploy():
    """ Creating and passing the archive to the web server """
    file = do_pack()
    if file is None:
        return False
    return do_deploy(file)
