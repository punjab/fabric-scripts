"""
Generate a report of all the IPs downloaded so far. This script is run via a fabric call.
"""
import socket
import sys
import glob

def lookup(addr):
  """Lookup address for ip"""
  try:
    return socket.gethostbyaddr(addr)[0]
  except socket.herror:
    return None

# return sys.argv[1]

def ip2url(fname):
  """open file and convert all lines to urls"""
  s = ""
  f =  open(fname)
  for l in f:
    line = str(l).strip()
    if line:
      s += (str(line) + " : " + str(lookup(line)) + "\n")
  f.close()
  return s
  
if __name__ == '__main__':
  result = open('result.txt', "w")
  for name in glob.glob('*.ubc.ca/*'):
    result.write( "\n")
    result.write( name + "\n" )
    result.write( '==========================================\n')
    result.write(ip2url(name))
  result.close()