# vim: ts=4 sw=4 et

from cloudify.decorators import *
import cloudify.manager
from cosmo.events import send_event
from cosmo_plugin_openstack_common import with_neutron_client

@operation
@with_logger
@with_neutron_client
def create_in_network(__source_properties, __target_cloudify_id, logger, neutron_client, **kwargs):
    port = __source_properties['port']
    network_id = cloudify.manager.get_node_state(__target_cloudify_id)['external_id']
    logger.debug('port.create_in_network(): port={0} network_id={1}'.format(port, network_id))
    neutron_client.create_port({
        'port': {
            'name': port['name'],
            'network_id': network_id,
        }
    })

@operation
@with_neutron_client
def delete(port, neutron_client, **kwargs):
    neutron_client.delete_port(neutron_client.cosmo_get_named('port', port['name'])['id'])

@operation
def send_started(__cloudify_id, **kwargs):
    send_event(__cloudify_id, "port-X", "port status", "state", "running")

