#!/usr/bin/env python
# vim: ts=4 sw=4 et

import unittest

import cosmo_plugin_openstack_common as os_common

import cloudify_plugin_openstack_neutron_provisioner.port as cfy_port
import cloudify_plugin_openstack_neutron_provisioner.network as cfy_net

class OpenstackNeutronTest(os_common.TestCase):

    @unittest.skip("have to update the test code")
    def test_port(self):
        name = self.name_prefix + 'the_port'
        network = self.create_network('for_port')
        subnet = self.create_subnet('for_port', '10.11.12.0/24', network=network)

        self.assertThereIsNo('port', name=name)

        __cloudify_id = '__cloudify_id_' + name + '_port'
        __target_cloudify_id = '__cloudify_id_' + name + '_net'
        network_node_state = self.nodes_data[__target_cloudify_id] 
        network_node_state['external_id'] = network['id']

        cfy_port.create_in_network(
            __source_properties = {'port': {'name': name}},
            __target_cloudify_id = __target_cloudify_id
        )
        self.assertThereIsOne('port', name=name)

        cfy_port.delete(port={'name': name})
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
        cfy_net.create(__cloudify_context=mock_ctx)

        net = self.assertThereIsOneAndGet('network', name=name)
        self.assertTrue(net['admin_state_up'])
        return

        cfy_net.stop(network)
        net = self.assertThereIsOneAndGet('network', name=name)
        self.assertFalse(net['admin_state_up'])

        cfy_net.start(network)
        net = self.assertThereIsOneAndGet('network', name=name)
        self.assertTrue(net['admin_state_up'])

        cfy_net.delete(network={'name': name})
        self.assertThereIsNo('network', name=name)

if __name__ == '__main__':
    unittest.main()
