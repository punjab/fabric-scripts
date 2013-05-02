from __future__ import with_statement
from fabric.api import *
from fabric.api import task
from fabric.contrib.files import exists

env.use_ssh_config = True # read ~/.ssh/.sshconfig
#env.hosts = ['']

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

def open_port(sourceip, number, protocol='tcp'):
    """ Open a given port in the firewall"""
    # Get the line before the rule thar rejects ALL
    line = sudo('iptables --line-numbers -vnLRH-Firewall-1-INPUT | grep REJECT | awk \'{print $1}\'')
    # Insert the new rule in that line pushing that line to the next line
    sudo('iptables -I RH-Firewall-1-INPUT %(line)s -s %(sourceip)s -p %(protocol)s --dport %(number)s -j ACCEPT' % {'number': number, 'protocol': protocol, 'line': line, 'sourceip': sourceip})
    sudo('service iptables save')
    sudo('service iptables restart')

@task
def check_ports():
    """ Get result of iptables -L"""
    sudo('iptables -L')

@task
def firewall(sourceip, number, protocol='tcp'):
    """Run open_port followed by check_ports """
    open_port(sourceip, number, protocol='tcp')
    check_ports()

@task
def restart_zabbix():
    """restart zabbix with new configuration"""
    sudo('killall zabbix_agentd')
    run('sleep 5')
    sudo('/usr/local/sbin/zabbix_agentd -c /usr/local/etc/zabbix_agentd.conf')
    
@task 
def gather_intel():
    """ main intel function """
    # read_hostfile()
    distribute_keys()
    get_stats()
    # list_connections()
    # local("python lib/ip2url.py")
    clean()