# vim: ts=4 sw=4 et

from cloudify.decorators import operation
from cosmo_plugin_openstack_common import with_neutron_client

def _find_network_in_related_nodes(ctx, neutron_client):
    networks_ids = [n['id'] for n in neutron_client.list_networks()['networks']]
    ret = []
    for runtime_properties in ctx.capabilities.get_all().values():
        external_id = runtime_properties.get('external_id')
        if external_id in networks_ids:
            ret.append(external_id)
    if len(ret) != 1:
        # TODO: better message
        raise RuntimeError("Failed to find port's network")
    return ret[0]


@operation
@with_neutron_client
def create(ctx, neutron_client, **kwargs):
    port = {
        'name': ctx.node_id,
        'network_id': _find_network_in_related_nodes(ctx, neutron_client),
    }
    port.update(ctx.properties['port'])
    p = neutron_client.create_port({'port': port})['port']
    ctx['external_id'] = p['id']
    ctx.set_started()

@operation
@with_neutron_client
def delete(ctx, neutron_client, **kwargs):
    neutron_client.delete_port(ctx.runtime_properties['external_id'])
    ctx.set_stopped()

@operation
@with_neutron_client
def connect_security_group(ctx, neutron_client, **kwargs):
    # WARNING: non-atomic operation
    port = neutron_client.cosmo_get('port', id=ctx.runtime_properties['external_id'])
    ctx.logger.info("connect_security_group(): related={0}".format(ctx.related.runtime_properties))
    sgs = port['security_groups'] + [ctx.related.runtime_properties['external_id']]
    neutron.update_port(port_id, {'port': {'security_groups': sgs}})
