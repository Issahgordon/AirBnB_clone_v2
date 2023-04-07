#!/usr/bin/env python3
"""Fabric script that distributes an archive to your web servers,
   using the function do_deploy"""

from fabric.api import *
from os.path import exists, basename, splitext

env.user = 'ubuntu'
env.hosts = ['<IP web-01>', '<IP web-02>']

def do_deploy(archive_path):
    """Distributes an archive to your web servers"""

    # Check if file exists
    if not exists(archive_path):
        return False

    # Get archive filename
    archive_filename = basename(archive_path)
    # Get archive basename without extension
    archive_basename = splitext(archive_filename)[0]

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")

        # Create directory to uncompress archive
        run("sudo mkdir -p /data/web_static/releases/{}/".format(archive_basename))

        # Uncompress the archive
        run("sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
            .format(archive_filename, archive_basename))

        # Delete the archive from the web server
        run("sudo rm /tmp/{}".format(archive_filename))

        # Move contents of web_static to web_static_<version>
        run("sudo mv /data/web_static/releases/{}/web_static/* "
            "/data/web_static/releases/{}/"
            .format(archive_basename, archive_basename))

        # Remove web_static directory
        run("sudo rm -rf /data/web_static/releases/{}/web_static".format(archive_basename))

        # Delete symbolic link /data/web_static/current
        run("sudo rm -rf /data/web_static/current")

        # Create new symbolic link /data/web_static/current
        run("sudo ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(archive_basename))

        print("New version deployed!")
        return True

    except Exception as e:
        print(e)
        return False

