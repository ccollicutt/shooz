# shooz

>"Our Lady of the Killer Shooz"
>-- Brasyl, Ian McDonald

## About

This inventory script does not query OpenStack nova directly. Instead it generates an inventory based on the hosts file which is setup very similarily to how Ansible does it's hosts file. Then that inventory is fed to Ansible, and the initial playbook used will use nova_compute, add_hosts, and set_fact to instantiate the virtual machiens and update the in-memory Ansible inventory so that Ansible can actually ssh into the instances.

I suppose it's more of a workflow than a full blown inventory-nova script.

## Hosts file format

Currently must look like this:

```bash
[openstack_instances]
servername flavor_id=int group=string
```

## Minimum playbook

The [example playbook](example.yml) shows the minium needed to use this workflow.

In order to use `nova_compute` you will have to setup the proper variables as well.

## Gotchas

* I don't think using a single host (ie. --host) would work with this workflow, so the inventory script doesn't support it

## Acknowledgements

* https://github.com/lukaspustina/dynamic-inventory-for-ansible-with-openstack
* https://github.com/ansible/ansible/blob/devel/plugins/inventory/nova.py
