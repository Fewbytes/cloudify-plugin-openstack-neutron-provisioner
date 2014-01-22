#!/usr/bin/env python
# vim: ts=4 sw=4 et

import unittest

import cosmo_plugin_openstack_common as os_common

import cloudify_plugin_openstack_neutron_provisioner.port as cfy_port

class OpenstackNeutronPortTest(os_common.TestCase):

    @os_common.with_neutron_client
    def test_port(self, neutron_client):
        name = self.name_prefix + 'the_port'
        network = self.create_network('for_port')

        self.assertEquals(0, len(list(neutron_client.cosmo_list('port', name=name))))

        cfy_port.create(port={'name': name}, network=network)
        self.assertEquals(1, len(list(neutron_client.cosmo_list('port', name=name))))

        cfy_port.delete(port={'name': name})
        self.assertEquals(0, len(list(neutron_client.cosmo_list('port', name=name))))


if __name__ == '__main__':
    # tests_config = os_common.TestsConfig().get()
    unittest.main()
