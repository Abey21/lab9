import unittest
import re
import ipaddress
from napalm import get_network_driver

def getconfig(IP, user, password):
    """
    Fetch running config from the router using Napalm.
    """
    driver = get_network_driver('ios')
    iosv12 = driver(IP, user, password)
    iosv12.open()
    ios_output = iosv12.get_config(retrieve='running')
    iosv12.close()
    return ios_output['running']

def testLoopback():
    """
    Test if Loopback99 interface has the correct IP and subnet.
    """
    config = getconfig('198.51.100.13', 'lab', 'lab123')  # Router 3's management IP
    loopback_pattern = r'interface Loopback99\s+ip address\s+(\d+\.\d+\.\d+\.\d+)\s+(\d+\.\d+\.\d+\.\d+)'
    loopback_match = re.search(loopback_pattern, config)
    
    if loopback_match:
        ip = loopback_match.group(1)
        subnet = ipaddress.IPv4Network('0.0.0.0/' + loopback_match.group(2)).prefixlen
        return str(ip) + '/' + str(subnet)
    else:
        raise ValueError("Loopback99 IP and subnet not found.")

def testAreas():
    """
    Test if the router has only a single OSPF area.
    """
    config = getconfig('198.51.100.11', 'lab', 'lab123')  # Router 1's management IP
    area_pattern = r'area.\d+'
    area_matches = re.findall(area_pattern, config)
    areas = set(area_matches)
    
    return len(areas) == 1

def pingTest():
    """
    Test if the ping from one router to another is successful.
    """
    driver = get_network_driver('ios')
    iosv12 = driver('198.51.100.12', 'lab', 'lab123')  # Router 2's management IP

    iosv12.open()
    ios_output = iosv12.ping('198.51.100.15')  # Router 5's loopback IP
    iosv12.close()

    return isinstance(ios_output, dict)

class RouterTests(unittest.TestCase):
    
    def test_loopbackTest(self):
        """
        Test if the Loopback99 IP and subnet match the expected values.
        """
        self.assertEqual(testLoopback(), '10.1.3.1/24')  # Expected IP from your configuration
    
    def test_areas(self):
        """
        Test if there is only a single OSPF area configured.
        """
        self.assertTrue(testAreas())
    
    def test_ping(self):
        """
        Test if the ping from Router 2 to Router 5 is successful.
        """
        self.assertTrue(pingTest())

if __name__ == '__main__':
    unittest.main()
