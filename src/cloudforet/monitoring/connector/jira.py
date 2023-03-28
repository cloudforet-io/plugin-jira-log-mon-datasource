import logging
import requests
import datetime
from requests.auth import HTTPBasicAuth

from spaceone.core.utils import iso8601_to_datetime
from cloudforet.monitoring.error import *

__all__ = ['JiraConnector']
_LOGGER = logging.getLogger(__name__)


class JiraConnector(object):

    def __init__(self, *args, **kwargs):
        self.url = kwargs.get('url', False)
        email = kwargs.get('email', False)
        api_token = kwargs.get('api_token', False)

        if self.url is False or email is False or api_token is False:
            raise ERROR_INVALID_JIRA_CREDENTIAL(url={self.url}, email={email}, api_token={api_token})

        self.auth = HTTPBasicAuth(email, api_token)
        self.headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    def list_issues(self, params):
        query = params.get('query', {})

        if query:
            issue_url = f'{self.url}/rest/api/3/search'
            jira_search_params = {
                'jql': self._generate_jql(params)
            }
            response = requests.get(issue_url, headers=self.headers, params=jira_search_params, auth=self.auth)

            if response.status_code == 200:
                return response.json().get('issues', [])
            else:
                _LOGGER.debug(response.text)
                return []
        else:
            _LOGGER.debug('JIRA Query is empty')
            return []

    def list_issue_change_logs(self, issue_id):
        changelog_url = f'{self.url}/rest/api/3/issue/{issue_id}/changelog'

        response = requests.get(changelog_url, headers=self.headers, auth=self.auth)

        if response.status_code == 200:
            _values = response.json().get('values', [])
            _values.reverse()
            return _values
        else:
            _LOGGER.debug(response.text)
            return []

    def _generate_jql(self, params):
        jql_list = []
        query = params.get('query', {})
        start, end = self.get_start_end_time(params.get('start'), params.get('end'))

        if start and end:
            jql_list.append(f'(created >= "{start}" AND created <= "{end}")')

        if query.get('jql'):
            jql_list.append(query.get('jql'))

        return ' AND '.join(jql_list)

    @staticmethod
    def get_start_end_time(start, end):
        try:
            _start = start.strftime('%Y/%m/%d')
            _end = end.strftime('%Y/%m/%d')
            return _start, _end

        except Exception as e:
            print(e)
            return None, None
