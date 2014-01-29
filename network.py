# vim: ts=4 sw=4 et

from cloudify.decorators import *
from cosmo.events import send_event, get_cosmo_properties
from cosmo_plugin_openstack_common import with_neutron_client

@operation
@with_logger
@with_neutron_client
@with_node_state
def create(__cloudify_id, network, node_state, logger, neutron_client, **kwargs):
    logger.debug('network.create(): network={0}'.format(network))

    if _get_network_by_name(neutron_client, network['name']):
        raise RuntimeError("Can not create network with name '{0}' because network with such name already exists"
                           .format(network['name']))

    net = neutron_client.create_network({
        'network': {
            'name': network['name'],
            'admin_state_up': True
        }
    })['network']
    node_state['external_id'] = net['id']
    # XXX: not really a host, signifies event origin name for riemann
    host = get_cosmo_properties()['ip']
    # TODO: change host to "network-NAME"
    send_event(__cloudify_id, host, "network status", "state", "running")

@operation
@with_neutron_client
def start(network, neutron_client, **kwargs):
    net = _get_network_by_name(neutron_client, network['name'])
    neutron_client.update_network(net['id'], {
        'network': {
            'admin_state_up': True
        }
    })

@operation
@with_neutron_client
def stop(network, neutron_client, **kwargs):
    net = _get_network_by_name(neutron_client, network['name'])
    neutron_client.update_network(net['id'], {
        'network': {
            'admin_state_up': False
        }
    })


@operation
@with_neutron_client
def delete(network, neutron_client, **kwargs):
    net = _get_network_by_name(neutron_client, network['name'])
    neutron_client.delete_network(net['id'])


def _get_network_by_name(neutron_client, name):
    # TODO: check whether neutron_client can get networks only named `name`
    matching_networks = neutron_client.list_networks(name=name)['networks']

    if len(matching_networks) == 0:
        return None
    if len(matching_networks) == 1:
        return matching_networks[0]
    raise RuntimeError("Lookup of network by name failed. There are {0} networks named '{1}'"
                       .format(len(matching_networks), name))


def _get_network_by_name_or_fail(neutron_client, name):
    network = _get_network_by_name(neutron_client, name)
    if network:
        return network
    raise ValueError("Lookup of network by name failed. Could not find a network with name {0}".format(name))
