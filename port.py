# vim: ts=4 sw=4 et

# Channge later to:
from cloudify.decorators import operation, with_logger
# from celery import task

from cosmo.events import send_event

import cosmo_plugin_openstack_common as os_common
with_neutron_client = os_common.with_neutron_client


@operation
@with_logger
@with_neutron_client
def create_in_network(__source_properties, __target_properties, logger, neutron_client, **kwargs):
    port = __source_properties['port']
    network = __target_properties['network']
    logger.debug('port.create_in_network(): port={0} network={1}'.format(port, network))
    neutron_client.create_port({
        'port': {
            'name': port['name'],
            'network_id': neutron_client.cosmo_get_named('network', network['name'])['id'],
        }
    })

@operation
@with_neutron_client
def delete(port, neutron_client, **kwargs):
    neutron_client.delete_port(neutron_client.cosmo_get_named('port', port['name'])['id'])

@operation
def send_started(__cloudify_id, **kwargs):
    send_event(__cloudify_id, "port-X", "port status", "state", "running")

