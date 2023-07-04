#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_staic.py that distributes
archive to web servers
162560-web-01 100.24.205.74
162560-web-02 34.204.101.28
"""

from fabric.api import put, run, env
from os.path import exists
env.hosts = ['3.84.237.43', '100.25.180.143']


def do_peloy(archive_path):
    """Distributes an archive to the web servers"""
    if exists(archive_path) is False:
        return False
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, "/tmp")
        run("mkdir -p {}{}/".format(path, no_ext))
        run("tar -xzf /tmp/{} -C {}{}/".format(file_n, path, no_ext))
        run("rm /tmp/{}".format(file_n))
        run("mv {0}{1}/web_static/* {0}{1}/".format(path, no_ext))
        run("rm -rf {}{}/web_static".format(path, no_ext))
        run("rm -rf /data/web_static/current")
        run("ln -s {}{}/ /data/web_static/current".format(path, no_ext))
        return True
    except Exception:
        return False
