import os
import logging
import time
import datetime

from spaceone.core import utils, config
from spaceone.tester import TestCase, print_json, to_json
from google.protobuf.json_format import MessageToDict

_LOGGER = logging.getLogger(__name__)

URL = os.environ.get('URL', None)
EMAIL = os.environ.get('EMAIL', None)
API_TOKEN = os.environ.get('API_TOKEN', None)
PROJECT = os.environ.get('PROJECT', None)

if API_TOKEN == None or EMAIL == None or URL == None or PROJECT == None:
    print("""
##################################################
# ERROR
#
# Configure your JIRA Token first for test
# How to create API KEY:
# - https://github.com/cloudforet-io/plugin-jira-log-mon-datasource/tree/master/docs/admin-guide
##################################################
example)

export URL=<YOUR atlassian url>
export EMAIL=<YOUR_atlassian email>
export API_TOKEN=<YOUR_API_TOKEN>
export PROJECT=<YOUR Project Code>
""")
    exit


class TestJiraMonDataSource(TestCase):
    config = utils.load_yaml_from_file(
        os.environ.get('SPACEONE_TEST_CONFIG_FILE', './config.yml'))
    endpoints = config.get('ENDPOINTS', {})
    secret_data = {
        'url': URL,
        'email': EMAIL,
        'api_token': API_TOKEN,
        'project': PROJECT
    }

    def test_init(self):
        v_info = self.monitoring.DataSource.init({'options': {}})
        print_json(v_info)

    def test_verify(self):
        options = {}
        self.monitoring.DataSource.verify({'options': options, 'secret_data': self.secret_data})

    def test_log(self):
        options = {}

        resource_stream = self.monitoring.Log.list({
            'start': '2023-03-08',
            'end': '2023-03-08',
            'options': options,
            'secret_data': self.secret_data,
            'query': {
                'jql': 'project=GCPSVC AND labels in (cloud-svc-63ec986aa6e0)'
            }
        })

        for res in resource_stream:
            print_json(res)
