import unittest
import re
import ipaddress
from napalm import get_network_driver

def fetch_config(IP, username, password):
    """
    Retrieve running config from the router using Napalm.
    """
    driver = get_network_driver('ios')
    router = driver(IP, username, password)

    router.open()
    router_output = router.get_config(retrieve='running')
    router.close()

    return router_output['running']

def validate_loopback_ip():
    """
    Validate if Loopback99 interface has the correct IP and subnet.
    """
    config = fetch_config('198.51.100.13', 'lab', 'lab123')  # Router 3's management IP
    loopback_pattern = r'interface Loopback99\s+ip address\s+(\d+\.\d+\.\d+\.\d+)\s+(\d+\.\d+\.\d+\.\d+)'
    loopback_match = re.search(loopback_pattern, config)

    if loopback_match:
        ip = loopback_match.group(1)
        subnet = ipaddress.IPv4Network('0.0.0.0/' + loopback_match.group(2)).prefixlen
        return str(ip) + '/' + str(subnet)
    else:
        raise ValueError("Loopback99 IP and subnet not found.")

def check_single_area():
    """
    Check if the router has only a single OSPF area configured.
    """
    config = fetch_config('198.51.100.11', 'lab', 'lab123')  # Router 1's management IP
    area_pattern = r'area.\d+'
    area_matches = re.findall(area_pattern, config)
    areas = set(area_matches)

    return len(areas) == 1

def verify_ping():
    """
    Verify if the ping from one router to another is successful.
    """
    driver = get_network_driver('ios')
    router = driver('198.51.100.12', 'lab', 'lab123')  # Router 2's management IP

    router.open()
    ping_response = router.ping('198.51.100.15')  # Router 5's loopback IP
    router.close()

    return isinstance(ping_response, dict)

class RouterTestCases(unittest.TestCase):

    def test_loopback_ip(self):
        """
        Test to verify the Loopback99 IP and subnet are correct.
        """
        self.assertEqual(validate_loopback_ip(), '10.1.3.1/24')  # Expected IP from your configuration

    def test_ospf_area_check(self):
        """
        Test to ensure there is only one OSPF area configured.
        """
        self.assertTrue(check_single_area())

    def test_ping_functionality(self):
        """
        Test to ensure the ping from Router 2 to Router 5 is successful.
        """
        self.assertTrue(verify_ping())

if __name__ == '__main__':
    unittest.main()
