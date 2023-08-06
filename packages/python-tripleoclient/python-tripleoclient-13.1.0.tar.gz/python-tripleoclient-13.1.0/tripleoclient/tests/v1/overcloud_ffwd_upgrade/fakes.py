#   Copyright 2018 Red Hat, Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

import mock
from osc_lib.tests import utils

from tripleoclient import plugin
from tripleoclient.tests import fakes


class FakeClientWrapper(object):

    def __init__(self):
        self._instance = mock.Mock()
        self.object_store = FakeObjectClient()

    def messaging_websocket(self, queue="tripleo"):
        return fakes.FakeWebSocket()


class FakeObjectClient(object):

    def __init__(self):
        self._instance = mock.Mock()
        self.put_object = mock.Mock()

    def get_object(self, *args):
        return


class TestFFWDUpgradePrepare(utils.TestCommand):

    def setUp(self):
        super(TestFFWDUpgradePrepare, self).setUp()

        self.app.client_manager.auth_ref = mock.Mock(auth_token="TOKEN")
        self.app.client_manager.baremetal = mock.Mock()
        self.app.client_manager.orchestration = mock.Mock()
        workflow = execution = mock.Mock()
        execution.id = "IDID"
        workflow.executions.create.return_value = execution
        self.app.client_manager.workflow_engine = workflow
        tc = self.app.client_manager.tripleoclient = FakeClientWrapper()
        tc.create_mistral_context = plugin.ClientWrapper(
            instance=fakes.FakeInstanceData
        ).create_mistral_context


class TestFFWDUpgradeRun(utils.TestCommand):

    def setUp(self):
        super(TestFFWDUpgradeRun, self).setUp()

        self.app.client_manager.auth_ref = mock.Mock(auth_token="TOKEN")
        self.app.client_manager.workflow_engine = mock.Mock()
        self.app.client_manager.orchestration = mock.Mock()
        tc = self.app.client_manager.tripleoclient = FakeClientWrapper()
        tc.create_mistral_context = plugin.ClientWrapper(
            instance=fakes.FakeInstanceData
        ).create_mistral_context


class TestFFWDUpgradeConverge(utils.TestCommand):

    def setUp(self):
        super(TestFFWDUpgradeConverge, self).setUp()

        self.app.client_manager.auth_ref = mock.Mock(auth_token="TOKEN")
        self.app.client_manager.baremetal = mock.Mock()
        self.app.client_manager.orchestration = mock.Mock()
        workflow = execution = mock.Mock()
        execution.id = "IDID"
        workflow.executions.create.return_value = execution
        self.app.client_manager.workflow_engine = workflow
        tc = self.app.client_manager.tripleoclient = FakeClientWrapper()
        tc.create_mistral_context = plugin.ClientWrapper(
            instance=fakes.FakeInstanceData
        ).create_mistral_context
