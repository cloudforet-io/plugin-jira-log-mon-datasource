import logging
import requests
from requests.auth import HTTPBasicAuth

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

    def list_issues(self, query):
        issue_url = f'{self.url}/rest/api/3/search'
        jira_search_params = {
            'jql': query.get('jql')
        }

        response = requests.get(issue_url, headers=self.headers, params=jira_search_params, auth=self.auth)

        if response.status_code == 200:
            return response.json().get('issues', [])
        else:
            _LOGGER.debug(response.text)
            return []

    def list_issue_change_logs(self, issue_id):
        changelog_url = f'{self.url}/rest/api/3/issue/{issue_id}/changelog'

        response = requests.get(changelog_url, headers=self.headers, auth=self.auth)

        if response.status_code == 200:
            return response.json().get('values', [])
        else:
            _LOGGER.debug(response.text)
            return []