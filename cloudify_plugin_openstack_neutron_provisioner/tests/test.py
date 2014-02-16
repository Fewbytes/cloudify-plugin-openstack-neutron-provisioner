#!/usr/bin/env python
# vim: ts=4 sw=4 et

import unittest

from cloudify.context import ContextCapabilities
from cloudify.mocks import MockCloudifyContext

import cosmo_plugin_openstack_common as os_common

import cloudify_plugin_openstack_neutron_provisioner.network as cfy_net
import cloudify_plugin_openstack_neutron_provisioner.port as cfy_port
import cloudify_plugin_openstack_neutron_provisioner.router as cfy_rtr
import cloudify_plugin_openstack_neutron_provisioner.security_group as cfy_sg
import cloudify_plugin_openstack_neutron_provisioner.subnet as cfy_sub

class OpenstackNeutronTest(os_common.TestCase):

    def test_port(self):
        name = self.name_prefix + 'the_port'
        network = self.create_network('for_port')
        subnet = self.create_subnet('for_port', '10.11.12.0/24', network=network)

        ctx = MockCloudifyContext(
            node_id = '__cloudify_id_' + name + '_port',
            properties = {'port': {'name': name}},
            capabilities = ContextCapabilities({
                'net_node': {
                    'external_id': network['id']
                }
            })
        )

        cfy_port.create(ctx)
        self.assertThereIsOne('port', name=name)

        cfy_port.delete(ctx)
        self.assertThereIsNo('port', name=name)

    def test_network(self):
        name = self.name_prefix + 'net'

        self.assertThereIsNo('network', name=name)

        mock_ctx = {
            'node_id': '__cloudify_id_' + name,
            'node_properties': {
                'network': {'name': name}
            }
        }

        ctx = MockCloudifyContext(
            node_id = '__cloudify_id_' + name,
            properties = {'network': {'name': name}},
        )

        cfy_net.create(ctx)

        net = self.assertThereIsOneAndGet('network', name=name)
        self.assertTrue(net['admin_state_up'])

        cfy_net.stop(ctx)
        net = self.assertThereIsOneAndGet('network', name=name)
        self.assertFalse(net['admin_state_up'])

        cfy_net.start(ctx)
        net = self.assertThereIsOneAndGet('network', name=name)
        self.assertTrue(net['admin_state_up'])

        cfy_net.delete(ctx)
        self.assertThereIsNo('network', name=name)

if __name__ == '__main__':
    unittest.main()
