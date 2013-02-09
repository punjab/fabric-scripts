from fabric.api import *
from fabric.api import task
from fabric.operations import get
env.use_ssh_config = True # read ~/.ssh/.sshconfig

import time
from os.path import basename, exists

env.hosts = ['mywebapp.com']
env.dbname = 'mydatabase'
env.dbuser = 'myusername'
env.dbpass = 'mypassword'

@task(default=True)
def backup_mysql():
    '''Backup MySQL database from remote server to local host'''
    date = time.strftime('%Y%m%d%H%M%S')
    filename = '/tmp/%(database)s-backup-%(date)s.sql.gz' % { 
        'database': env.dbname,
        'date': date
    }

    if exists(filename):
        run('rm "%s"' % filename)
        
    run('mysqldump -u %(username)s -p%(password)s %(database)s | gzip > %(filename)s' % {
            'username': env.dbuser,
            'password': env.dbpass,
            'database': env.dbname,
            'filename': filename
    })
    
    get(filename, os.path.basename(filename))
    run('rm "%s"' % filename)