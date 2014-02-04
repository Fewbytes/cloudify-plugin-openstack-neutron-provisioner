# vim: ts=4 sw=4 et

from cloudify.decorators import operation
from cosmo_plugin_openstack_common import with_neutron_client

@operation
@with_neutron_client
def create(ctx, neutron_client, **kwargs):
    subnet = {
        'network_id': ctx.capabilities['external_id']
    }
    subnet.update(ctx.properties['subnet'])

    s = neutron_client.create_subnet({'subnet': subnet})['subnet']
    ctx.runtime_properties['external_id'] = s['id']
    ctx.set_started()

@operation
@with_neutron_client
def delete(ctx, neutron_client, **kwargs):
    neutron_client.delete_subnet(ctx.runtime_properties['external_id'])
