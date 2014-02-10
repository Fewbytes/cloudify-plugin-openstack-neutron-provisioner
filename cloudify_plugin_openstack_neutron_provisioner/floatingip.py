# vim: ts=4 sw=4 et

from cloudify.decorators import operation
from cosmo_plugin_openstack_common import with_neutron_client

@operation
@with_neutron_client
def create(ctx, neutron_client, **kwargs):
    floatingip = {
        # No defaults
    }
    floatingip.update(ctx.properties['floatingip'])
    if 'floating_network_name' in floatingip:
        floatingip['floating_network_id'] = neutron_client.cosmo_get_named('network', floatingip['floating_network_name'])
        del floatingip['floating_network_name']

    fip = neutron_client.create_floatingip({'floatingip': floatingip})['floatingip']
    ctx.runtime_properties['external_id'] = fip['id']
    ctx.runtime_properties['floating_ip_address'] = fip['floating_ip_address']
    ctx.logger.debug("Allocated Floating IP {0}".format(fip['floating_ip_address']))
    ctx.set_started()

@operation
@with_neutron_client
def delete(ctx, neutron_client, **kwargs):
    neutron_client.delete_floatingip(ctx.runtime_properties['external_id'])

