#!/usr/bin/python

import sys

try:
  import yaml
except:
  print "ERROR: Requires yaml"
  sys.exit(1)

try:
  from novaclient.v1_1 import client
except:
  print "ERROR: Need python-novaclient"
  sys.exit(1)

try:
    import json
except:
    import simplejson as json

# Want to use the same variable file as for with ansibles nova_compute which
# I am calling openstack_instances
OS_VARS = "./group_vars/openstack_instances"
OS_NOVA_VERSION = 2
OS_AUTH_SYSTEM = ""

def get_nova():
  """Open the config file and connect to nova"""

  try:
    os_config = open(OS_VARS, 'r')
    conf = yaml.load(os_config)
  except:
    print "ERROR: Could not load " + OS_VARS
    sys.exit(1)

  nova_client = client.Client(
      username = conf['os_username'],
      api_key = conf['os_password'],
      project_id = conf['os_tenant_name'],
      auth_url = conf['os_auth_url'],
      region_name = conf['os_region_name'],
      auth_system = OS_AUTH_SYSTEM
  )

  return nova_client

def add_host(vm_name, group, inventory, flavor=None, ip=None):
  """Add the host to the inventory"""

  if not group in inventory:
    inventory[group] = {
      'hosts' : [],
    }

  if not vm_name in inventory[group]:
    inventory[group]['hosts'].append(vm_name)

  if not vm_name in inventory['_meta']:
    inventory['_meta']['hostvars'][vm_name] = {}
    if flavor:
      inventory['_meta']['hostvars'][vm_name]['flavor_id'] = flavor
    if ip:
      inventory['_meta']['hostvars'][vm_name]['ansible_ssh_host'] = ip

def open_file(file_name):
  """Return a file handle"""

  try:
    f = open(file_name)
  except (OSError, IOError) as e:
    return False

  return f

def main(args):

  # initialize the inventory
  inventory = {}
  inventory['_meta'] = {}
  inventory['_meta']['hostvars'] = {}

  # Open the hosts file; assumes hosts file is in local directory the command
  # is being run from.
  f = open_file('./hosts')

  # Check to see if the server already exists in nova
  nc = get_nova()

  # Get all the servers
  nova_servers = nc.servers.findall()

  # FIXME: more pythonic error checking
  if f:
    for line in f.readlines():
      if line == "[openstack_instances]\n":
        group = line.replace("[", "")
        group = group.replace("]", "")
        group = group.replace("\n", "")
      # FIXME: test cases
      elif line.startswith("#"):
        break
      elif line.startswith("[") or line == "\n":
        break
      else:

        # Get the server name
        server = line.split()

        name = server[0]
        # FIXME
        # flavor_id=1
        flavor = server[1].split("=")[1]
        # group=somegroup
        group = server[2].split("=")[1]

        # FIXME: Should be in some kind of array
        add_host(vm_name=name, group=group, inventory=inventory )
        add_host(vm_name=name, group='openstack_instances', inventory=inventory)

        # Loop through the nova servers looking for name
        nova_server = None
        for s in nova_servers:
          if s.name == name:
            nova_server = s

        if nova_server:
          ip = nova_server.addresses['cybera'][0]['addr']
          add_host(vm_name=name, group='undefined', inventory=inventory, \
            flavor=flavor, ip=ip)
        else:
          # add flavor last
          add_host(vm_name=name, group='undefined', inventory=inventory, \
          flavor=flavor)
  else:
    print "ERROR: Could not find hosts file"
    sys.exit(1)

  print json.dumps(inventory, sort_keys=True, indent=4)

if __name__ == "__main__":
    main(sys.argv)
