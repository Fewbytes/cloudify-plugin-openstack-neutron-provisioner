# vim: ts=4 sw=4 et

from cloudify.decorators import operation
from cosmo_plugin_openstack_common import with_neutron_client

# Runs on "target" becuse it's in relationships.target_interfaces
# Since we're target, ctx.related is the "source".

@operation
@with_neutron_client
def create(ctx, neutron_client, **kwargs):
    port = {
        'network_id': ctx.capabilities['external_id']
    }
    port.update(ctx.properties['port'])
    p = neutron_client.create_port({'port': port})['port']
    ctx['external_id'] = p['id']
    ctx.set_started()

@operation
@with_neutron_client
def delete(port, neutron_client, **kwargs):
    neutron_client.delete_port(neutron_client.cosmo_get_named('port', port['name'])['id'])
