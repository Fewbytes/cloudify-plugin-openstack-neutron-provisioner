# vim: ts=4 sw=4 et

# Channge later to:
# from cloudify.decorators import operation
from celery import task

import cosmo_plugin_openstack_common as os_common
with_neutron_client = os_common.with_neutron_client


@task
@with_neutron_client
def create(port, network, neutron_client, **kwargs):
    neutron_client.create_port({
        'port': {
            'name': port['name'],
            'network_id': neutron_client.cosmo_get_named('network', network['name'])['id'],
        }
    })

@task
@with_neutron_client
def delete(port, neutron_client, **kwargs):
    neutron_client.delete_port(neutron_client.cosmo_get_named('port', port['name'])['id'])

