# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2019.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

import requests

from qiskit.providers import BaseBackend
from qiskit.providers.models import BackendConfiguration
from . import aqt_job
from . import qobj_to_aqt


class AQTSimulator(BaseBackend):

    def __init__(self, provider):
        self.url = 'http://0f4aa71c.ngrok.io/cirq'
        configuration = {
            'backend_name': 'aqt_qasm_simulator',
            'backend_version': '0.0.1',
            'url': self.url,
            'simulator': True,
            'local': False,
            'coupling_map': None,
            'description': 'aqt trapped ion device simulator',
            'basis_gates': ['rx', 'ry', 'rxx'],
            'memory': False,
            'n_qubits': 11,
            'conditional': False,
            'max_shots': 250,
            'open_pulse': False,
            'gates': [
                {
                    'name': 'TODO',
                    'parameters': [],
                    'qasm_def': 'TODO'
                }
            ]
        }

        # We will explain about the provider in the next section
        super().__init__(
            configuration=BackendConfiguration.from_dict(configuration),
            provider=provider)

    def run(self, qobj):
        aqt_json = qobj_to_aqt.qobj_to_aqt(
            qobj, self._provider.access_token)[0]
        res = requests.put(self.url, data=aqt_json)
        res.raise_for_status()
        response = res.json()
        if 'id' not in response:
            raise Exception
        job = aqt_job.AQTJob(self, response['id'], qobj=qobj)
        return job


class AQTDevice(BaseBackend):

    def __init__(self, provider):
        self.url = 'http://aqt-uibk-lintrap.ngrok.io/cirq'
        configuration = {
            'backend_name': 'aqt_innsbruck',
            'backend_version': '0.0.1',
            'url': self.url,
            'simulator': False,
            'local': False,
            'coupling_map': None,
            'description': 'aqt trapped ion device',
            'basis_gates': ['rx', 'ry', 'rxx', 'ms'],
            'memory': False,
            'n_qubits': 4,
            'conditional': False,
            'max_shots': 250,
            'open_pulse': False,
            'gates': [
                {
                    'name': 'TODO',
                    'parameters': [],
                    'qasm_def': 'TODO'
                }
            ]
        }
        # We will explain about the provider in the next section
        super().__init__(
            configuration=BackendConfiguration.from_dict(configuration),
            provider=provider)

    def run(self, qobj):
        aqt_json = qobj_to_aqt.qobj_to_aqt(
            qobj, self._provider.access_token)[0]
        res = requests.put(self.url, data=aqt_json)
        res.raise_for_status()
        response = res.json()
        if 'id' not in response:
            raise Exception
        job = aqt_job.AQTJob(self, response['id'], qobj=qobj)
        return job
