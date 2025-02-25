"""Integration tests for cc_ca_certs.

(This is ported from ``tests/cloud_tests//testcases/modules/ca_certs.yaml``.)

TODO:
* Mark this as running on Debian and Alpine (once we have marks for that)
* Implement testing for the RHEL-specific paths
"""
import os.path

import pytest

from tests.integration_tests.instances import IntegrationInstance
from tests.integration_tests.util import get_inactive_modules, verify_clean_log

USER_DATA = """\
#cloud-config
ca_certs:
  remove_defaults: true
  trusted:
    - |
      -----BEGIN CERTIFICATE-----
      MIIGJzCCBA+gAwIBAgIBATANBgkqhkiG9w0BAQUFADCBsjELMAkGA1UEBhMCRlIx
      DzANBgNVBAgMBkFsc2FjZTETMBEGA1UEBwwKU3RyYXNib3VyZzEYMBYGA1UECgwP
      d3d3LmZyZWVsYW4ub3JnMRAwDgYDVQQLDAdmcmVlbGFuMS0wKwYDVQQDDCRGcmVl
      bGFuIFNhbXBsZSBDZXJ0aWZpY2F0ZSBBdXRob3JpdHkxIjAgBgkqhkiG9w0BCQEW
      E2NvbnRhY3RAZnJlZWxhbi5vcmcwHhcNMTIwNDI3MTAzMTE4WhcNMjIwNDI1MTAz
      MTE4WjB+MQswCQYDVQQGEwJGUjEPMA0GA1UECAwGQWxzYWNlMRgwFgYDVQQKDA93
      d3cuZnJlZWxhbi5vcmcxEDAOBgNVBAsMB2ZyZWVsYW4xDjAMBgNVBAMMBWFsaWNl
      MSIwIAYJKoZIhvcNAQkBFhNjb250YWN0QGZyZWVsYW4ub3JnMIICIjANBgkqhkiG
      9w0BAQEFAAOCAg8AMIICCgKCAgEA3W29+ID6194bH6ejLrIC4hb2Ugo8v6ZC+Mrc
      k2dNYMNPjcOKABvxxEtBamnSaeU/IY7FC/giN622LEtV/3oDcrua0+yWuVafyxmZ
      yTKUb4/GUgafRQPf/eiX9urWurtIK7XgNGFNUjYPq4dSJQPPhwCHE/LKAykWnZBX
      RrX0Dq4XyApNku0IpjIjEXH+8ixE12wH8wt7DEvdO7T3N3CfUbaITl1qBX+Nm2Z6
      q4Ag/u5rl8NJfXg71ZmXA3XOj7zFvpyapRIZcPmkvZYn7SMCp8dXyXHPdpSiIWL2
      uB3KiO4JrUYvt2GzLBUThp+lNSZaZ/Q3yOaAAUkOx+1h08285Pi+P8lO+H2Xic4S
      vMq1xtLg2bNoPC5KnbRfuFPuUD2/3dSiiragJ6uYDLOyWJDivKGt/72OVTEPAL9o
      6T2pGZrwbQuiFGrGTMZOvWMSpQtNl+tCCXlT4mWqJDRwuMGrI4DnnGzt3IKqNwS4
      Qyo9KqjMIPwnXZAmWPm3FOKe4sFwc5fpawKO01JZewDsYTDxVj+cwXwFxbE2yBiF
      z2FAHwfopwaH35p3C6lkcgP2k/zgAlnBluzACUI+MKJ/G0gv/uAhj1OHJQ3L6kn1
      SpvQ41/ueBjlunExqQSYD7GtZ1Kg8uOcq2r+WISE3Qc9MpQFFkUVllmgWGwYDuN3
      Zsez95kCAwEAAaN7MHkwCQYDVR0TBAIwADAsBglghkgBhvhCAQ0EHxYdT3BlblNT
      TCBHZW5lcmF0ZWQgQ2VydGlmaWNhdGUwHQYDVR0OBBYEFFlfyRO6G8y5qEFKikl5
      ajb2fT7XMB8GA1UdIwQYMBaAFCNsLT0+KV14uGw+quK7Lh5sh/JTMA0GCSqGSIb3
      DQEBBQUAA4ICAQAT5wJFPqervbja5+90iKxi1d0QVtVGB+z6aoAMuWK+qgi0vgvr
      mu9ot2lvTSCSnRhjeiP0SIdqFMORmBtOCFk/kYDp9M/91b+vS+S9eAlxrNCB5VOf
      PqxEPp/wv1rBcE4GBO/c6HcFon3F+oBYCsUQbZDKSSZxhDm3mj7pb67FNbZbJIzJ
      70HDsRe2O04oiTx+h6g6pW3cOQMgIAvFgKN5Ex727K4230B0NIdGkzuj4KSML0NM
      slSAcXZ41OoSKNjy44BVEZv0ZdxTDrRM4EwJtNyggFzmtTuV02nkUj1bYYYC5f0L
      ADr6s0XMyaNk8twlWYlYDZ5uKDpVRVBfiGcq0uJIzIvemhuTrofh8pBQQNkPRDFT
      Rq1iTo1Ihhl3/Fl1kXk1WR3jTjNb4jHX7lIoXwpwp767HAPKGhjQ9cFbnHMEtkro
      RlJYdtRq5mccDtwT0GFyoJLLBZdHHMHJz0F9H7FNk2tTQQMhK5MVYwg+LIaee586
      CQVqfbscp7evlgjLW98H+5zylRHAgoH2G79aHljNKMp9BOuq6SnEglEsiWGVtu2l
      hnx8SB3sVJZHeer8f/UQQwqbAO+Kdy70NmbSaqaVtp8jOxLiidWkwSyRTsuU6D8i
      DiH5uEqBXExjrj0FslxcVKdVj5glVcSmkLwZKbEU1OKwleT/iXFhvooWhQ==
      -----END CERTIFICATE-----
"""


@pytest.mark.ubuntu
@pytest.mark.user_data(USER_DATA)
class TestCaCerts:
    def test_certs_updated(self, class_client: IntegrationInstance):
        """Test that /etc/ssl/certs is updated as we expect."""
        root = "/etc/ssl/certs"
        filenames = class_client.execute(["ls", "-1", root]).splitlines()
        unlinked_files = []
        links = {}
        for filename in filenames:
            full_path = os.path.join(root, filename)
            symlink_target = class_client.execute(["readlink", full_path])
            is_symlink = symlink_target.ok
            if is_symlink:
                links[filename] = symlink_target
            else:
                unlinked_files.append(filename)

        assert ["ca-certificates.crt"] == unlinked_files
        assert "cloud-init-ca-certs.pem" == links["a535c1f3.0"]
        assert (
            "/usr/share/ca-certificates/cloud-init-ca-certs.crt"
            == links["cloud-init-ca-certs.pem"]
        )

    def test_cert_installed(self, class_client: IntegrationInstance):
        """Test that our specified cert has been installed"""
        checksum = class_client.execute(
            "sha256sum /etc/ssl/certs/ca-certificates.crt"
        )
        assert (
            "78e875f18c73c1aab9167ae0bd323391e52222cc2dbcda42d129537219300062"
            in checksum
        )

    def test_clean_logs(self, class_client: IntegrationInstance):
        log = class_client.read_from_file("/var/log/cloud-init.log")
        verify_clean_log(log, ignore_deprecations=False)
        diff = {
            "apt-pipelining",
            "bootcmd",
            "chef",
            "disable-ec2-metadata",
            "disk_setup",
            "fan",
            "keyboard",
            "landscape",
            "lxd",
            "mcollective",
            "ntp",
            "package-update-upgrade-install",
            "phone-home",
            "power-state-change",
            "puppet",
            "rsyslog",
            "runcmd",
            "salt-minion",
            "snap",
            "timezone",
            "ubuntu_autoinstall",
            "ubuntu-advantage",
            "ubuntu-drivers",
            "update_etc_hosts",
            "write-files",
            "write-files-deferred",
        }.symmetric_difference(get_inactive_modules(log))
        assert (
            not diff
        ), f"Expected inactive modules do not match, diff: {diff}"
