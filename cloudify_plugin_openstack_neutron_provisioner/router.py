from cloudify.decorators import operation
from cosmo_plugin_openstack_common import with_neutron_client


@operation
@with_neutron_client
def create(ctx, neutron_client, **kwargs):
    """ Create a router.
    Optional relationship is to gateway network.
    Also supports `router.external_gateway_info.network_name`,
    which is translated to `router.external_gateway_info.network_id`.
    """

    ctx.logger.debug('router.create(): kwargs={0}'.format(kwargs))
    router = {
        'name': ctx.node_id,
    }
    router.update(ctx.properties['router'])

    # Probably will not be used. External network
    # is usually provisioned externally.
    if 'external_id' in ctx.capabilities:
        if 'external_gateway_info' not in router:
            router['external_gateway_info'] = {
                'enable_snat': True
            }
        router['external_gateway_info'][
            'network_id'] = ctx.capabilities['external_id']

    # Sugar: external_gateway_info.network_name ->
    # external_gateway_info.network_id
    if 'external_gateway_info' in router:
        egi = router['external_gateway_info']
        if 'network_name' in egi:
            egi['network_id'] = neutron_client.cosmo_get_named(
                'network', egi['network_name'])['id']
            del egi['network_name']

    r = neutron_client.create_router({'router': router})['router']

    ctx['external_id'] = r['id']
    ctx.set_started()


@operation
@with_neutron_client
def connect_subnet(ctx, neutron_client, **kwargs):
    neutron_client.add_interface_router(
        ctx.runtime_properties['external_id'],
        {'subnet_id': ctx.related.runtime_properties['external_id']}
    )


@operation
@with_neutron_client
def disconnect_subnet(ctx, neutron_client, **kwargs):
    neutron_client.remove_interface_router(
        ctx.runtime_properties['external_id'],
        {'subnet_id': ctx.related.runtime_properties['external_id']}
    )


@operation
@with_neutron_client
def delete(ctx, neutron_client, **kwargs):
    neutron_client.delete_router(ctx.runtime_properties['external_id'])
