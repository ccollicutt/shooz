# shooz

>"Our Lady of the Killer Shooz"
>-- Brasyl, Ian McDonald

## About

This Ansible inventory script uses the OpenStack credentials in ```group_vars/openstack_instances``` to connect to an OpenStack compute service and get a list of servers. Then it opens the ```./hosts``` file and uses the servers listed there to query OpenStack compute and obtain the ip address of each server, if they exist, by their name (as opposed to their uuid).

## group_vars/openstack_instances

This inventory script expects that there will be an Ansible variable file called ```openstack_instances```.

## Hosts file format

Currently must look like this:

```bash
[openstack_instances]
servername flavor_id=int group=string
```

## group_vars/openstack_instances

This script requires that your OpenStack credentials are in ```group_vars/openstack_instances```.

## Minimum playbook

The [example playbook](example.yml) shows the minium needed to use this workflow.

In order to use `nova_compute` you will have to setup the proper variables as well.

## Gotchas

* Single host not supported yet

## Acknowledgements

* https://github.com/lukaspustina/dynamic-inventory-for-ansible-with-openstack
* https://github.com/ansible/ansible/blob/devel/plugins/inventory/nova.py
