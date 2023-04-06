#!/usr/bin/python3
"""Distributes an archive to your web servers, using the function do_deploy"""
from fabric.contrib import files
from fabric.api import env, put, run, local
import os
import datetime

env.hosts = ['104.196.116.233', '54.165.130.77']


def do_pack():
    """Do_pack function"""
    today = datetime.datetime.now()
    file_local = 'versions/web_static_{}{}{}{}{}{}.tgz'.format(today.year,
                                                               today.month,
                                                               today.day,
                                                               today.hour,
                                                               today.minute,
                                                               today.second)

    local('mkdir -p versions')
    check = local('tar -cvzf {} web_static'.format(file_local))
    if check.failed:
        return None
    else:
        return file_local


def do_deploy(archive_path):
    """Function for deploy"""
    if not os.path.exists(archive_path):
        return False

    data_path = '/data/web_static/releases/'
    tmp = archive_path.split('.')[0]
    name = tmp.split('/')[1]
    dest = data_path + name

    try:
        put(archive_path, '/tmp')
        run('mkdir -p {}'.format(dest))
        run('tar -xzf /tmp/{}.tgz -C {}'.format(name, dest))
        run('rm -f /tmp/{}.tgz'.format(name))
        run('mv {}/web_static/* {}/'.format(dest, dest))
        run('rm -rf {}/web_static'.format(dest))
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(dest))
        return True
    except:
        return False


def deploy():
    """Compress and upload files to remote server."""
    path = do_pack()
    print(path)
    if path is None:
        return False

    return do_deploy(path)


deploy()
