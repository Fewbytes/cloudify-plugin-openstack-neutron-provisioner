#!/usr/bin/env python
# vim: ts=4 sw=4 et

import unittest

import cosmo_plugin_openstack_common as os_common

import cloudify_plugin_openstack_neutron_provisioner.port as cfy_port
import cloudify_plugin_openstack_neutron_provisioner.network as cfy_net

class OpenstackNeutronTest(os_common.TestCase):

    @os_common.with_neutron_client
    def test_port(self, neutron_client):
        name = self.name_prefix + 'the_port'
        network = self.create_network('for_port')
        subnet = self.create_subnet('for_port', '10.11.12.0/24', network=network)

        self.assertEquals(0, len(list(neutron_client.cosmo_list('port', name=name))))

        __target_cloudify_id = '__cloudify_id_' + name + '_net'
        network_node_state = self.nodes_data[__target_cloudify_id] 
        network_node_state['external_id'] = network['id']

        cfy_port.create_in_network(
            __source_properties={'port': {'name': name}},
            __target_cloudify_id = __target_cloudify_id
        )
        self.assertEquals(1, len(list(neutron_client.cosmo_list('port', name=name))))

        cfy_port.delete(port={'name': name})
        self.assertEquals(0, len(list(neutron_client.cosmo_list('port', name=name))))

    @os_common.with_neutron_client
    def test_network(self, neutron_client):
        name = self.name_prefix + 'net'
        network = {'name': name}

        self.assertThereIsNo('network', name=name)

        cfy_net.create('__cloudify_id_' + name, network)
        net = self.assertThereIsOneAndGet('network', name=name)
        self.assertTrue(net['admin_state_up'])

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
