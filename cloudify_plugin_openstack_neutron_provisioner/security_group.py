# vim: ts=4 sw=4 et

from cloudify.decorators import operation
from cosmo_plugin_openstack_common import with_neutron_client

@operation
@with_neutron_client
def create(ctx, neutron_client, **kwargs):
    security_group = {
        'description': None,
        'name': ctx.node_id,
    }
    security_group.update(ctx.properties['security_group'])
    sg = neutron_client.create_security_group({'security_group': security_group})['security_group']

    ctx['external_id'] = sg['id']
    ctx.set_started()

@operation
@with_neutron_client
def delete(security_group, neutron_client, **kwargs):
    neutron_client.delete_security_group(ctx.runtime_properties['external_id'])
