# vim: ts=4 sw=4 et

from cloudify.decorators import operation
from cosmo_plugin_openstack_common import with_neutron_client

@operation
@with_neutron_client
def create(ctx, neutron_client, **kwargs):
    network = {
        'admin_state_up': True,
        'name': ctx.node_id,
    }
    network.update(ctx.properties['network'])

    net = neutron_client.create_network({'network': network})['network']
    ctx['external_id'] = net['id']
    ctx.update()
    ctx.set_started()

@operation
@with_neutron_client
def start(ctx, neutron_client, **kwargs):
    neutron_client.update_network(ctx.runtime_properties['external_id'], {
        'network': {
            'admin_state_up': True
        }
    })

@operation
@with_neutron_client
def stop(ctx, neutron_client, **kwargs):
    neutron_client.update_network(ctx.runtime_properties['external_id'], {
        'network': {
            'admin_state_up': False
        }
    })

@operation
@with_neutron_client
def delete(ctx, neutron_client, **kwargs):
    neutron_client.delete_network(ctx.runtime_properties['external_id'])
