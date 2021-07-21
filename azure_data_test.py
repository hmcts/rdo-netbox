import unittest
import azure_data


class AzureVnetsTestCase(unittest.TestCase):
    def test_is_private_ip(self):
        ips = [
            ["192.168.1.23/32", True],
            ["10.168.1.0/30", True],
            ["193.168.1.23/32", False],
        ]
        ad = azure_data.AzureVnets()
        for i in ips:
            is_private = ad.is_private(i[0])
            self.assertEqual(is_private, i[1], "is_private({}) -> {} != {}".format(i[0], is_private, i[1]))

    def test_prefix_or_ip_supernet(self):
        ips = [
            ["10.24.0.129/32", "10.24.0.128/31"],
            ["10.168.1.0/30", "10.168.1.0/30"],
            ["192.168.1.23/32", "192.168.1.22/31"],
        ]
        ad = azure_data.AzureVnets()
        for i in ips:
            pref_or_snet = ad.prefix_or_ip_supernet(i[0])
            self.assertEqual(pref_or_snet, i[1], "supernet({}) -> {} != {}".format(i[0], pref_or_snet, i[1]))


if __name__ == '__main__':
    unittest.main()
