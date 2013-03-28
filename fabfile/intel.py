from __future__ import with_statement
from fabric.api import *
from fabric.api import task
from fabric.contrib.files import exists

env.use_ssh_config = True # read ~/.ssh/.sshconfig
# env.hosts = ['']

@task
def distribute_keys():
  """ Distribute keys to servers """
  local("ssh-copy-id -i ~/.ssh/id_rsa.pub %s@%s" % (env.user, env.host))
  
def read_hostfile(f="hosts.txt"):
  """ get the env.hosts from hosts.txt file in the same directory """
  env.hosts = open(f, 'r').readlines()
  
def list_connections():
  """list all the IPs the machine is connected to"""
  with cd("/tmp"):
    run("netstat -nat | awk '{ print $5}' | cut -d: -f1,2 | sed -e 's/[^0-9.:]*//g' | sort |  uniq > `echo $HOSTNAME`.txt")
    get(env.host+".txt")

def get_stats():
  """get hardware and software stats about a Linux machine"""
  with cd("/tmp"):
    run("lsb_release -d")
    run("cat /proc/cpuinfo |grep processor|wc -l")
    run("free -m")
    run("egrep --color 'Mem|Cache|Swap' /proc/meminfo")
    run("df -TH")
    run("ldd --version|grep ldd")
    run("perl -v |grep 'This is perl'")

@task
def clean():
  """ remove all folders """
  local("rm -rf *.ubc.ca")

@task(default=True)    
def gather_intel():
  """ main intel function """
  # read_hostfile()
  distribute_keys()
  get_stats()
  # list_connections()
  # local("python lib/ip2url.py")
  clean()
  