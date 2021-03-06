# vim: ts=4 sw=4 et

from cloudify.decorators import operation
from cosmo_plugin_openstack_common import with_neutron_client

# Create or use existing


@operation
@with_neutron_client
def create(ctx, neutron_client, **kwargs):

    # Already acquired?
    if ctx.runtime_properties.get('external_id'):
        ctx.logger.debug("Using already allocated Floating IP {0}".format(
            ctx.runtime_properties['floating_ip_address']))
        ctx.set_started()
        return

    floatingip = {
        # No defaults
    }
    floatingip.update(ctx.properties['floatingip'])

    # Sugar: ip -> (copy as is) -> floating_ip_address
    if 'ip' in floatingip:
        floatingip['floating_ip_address'] = floatingip['ip']
        del floatingip['ip']

    if 'floating_ip_address' in floatingip:
        fip = neutron_client.cosmo_get(
            'floatingip', floating_ip_address=floatingip['floating_ip_address'])
        ctx.runtime_properties['external_id'] = fip['id']
        ctx.runtime_properties['floating_ip_address'] = fip['floating_ip_address']
        ctx.runtime_properties['enable_deletion'] = False  # Not acquired here
        ctx.set_started()
        return

    # Sugar: floating_network_name -> (resolve) -> floating_network_id
    if 'floating_network_name' in floatingip:
        floatingip['floating_network_id'] = neutron_client.cosmo_get_named(
            'network', floatingip['floating_network_name'])['id']
        del floatingip['floating_network_name']

    fip = neutron_client.create_floatingip(
        {'floatingip': floatingip})['floatingip']
    ctx.runtime_properties['external_id'] = fip['id']
    ctx.runtime_properties['floating_ip_address'] = fip['floating_ip_address']
    # Acquired here -> OK to delete
    ctx.runtime_properties['enable_deletion'] = True
    ctx.logger.debug(
        "Allocated floating IP {0}".format(fip['floating_ip_address']))
    ctx.set_started()


@operation
@with_neutron_client
def delete(ctx, neutron_client, **kwargs):
    do_delete = bool(ctx.runtime_properties.get('enable_deletion'))
    op = ['Not deleting', 'Deleting'][do_delete]
    ctx.logger.debug("{0} floating IP {1}".format(
        op, ctx.runtime_properties['floating_ip_address']))
    if do_delete:
        neutron_client.delete_floatingip(ctx.runtime_properties['external_id'])
    ctx.set_stopped()
