#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import json

import mock

from sushy.resources.system.storage import drive
from sushy.tests.unit import base


class DriveTestCase(base.TestCase):

    def setUp(self):
        super(DriveTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('sushy/tests/unit/json_samples/drive.json') as f:
            self.conn.get.return_value.json.return_value = json.load(f)

        self.stor_drive = drive.Drive(
            self.conn,
            '/redfish/v1/Systems/437XR1138/Storage/1/Drives/32ADF365C6C1B7BD',
            redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.stor_drive._parse_attributes()
        self.assertEqual('1.0.2', self.stor_drive.redfish_version)
        self.assertEqual('32ADF365C6C1B7BD', self.stor_drive.identity)
        self.assertEqual('Drive Sample', self.stor_drive.name)
        self.assertEqual(899527000000, self.stor_drive.capacity_bytes)
