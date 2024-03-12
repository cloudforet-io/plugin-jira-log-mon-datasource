import logging
import requests
import datetime
from requests.auth import HTTPBasicAuth
from spaceone.core.utils import iso8601_to_datetime
from cloudforet.monitoring.connector.base import JiraBaseConnector
from cloudforet.monitoring.error import *

__all__ = ['JiraConnector']
_LOGGER = logging.getLogger(__name__)


class JiraConnector(JiraBaseConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def list_issues(self, search_field_id, resource_id, start, end):
        url = "/rest/api/3/search"
        jira_search_params = {
            'jql': self._generate_jql(search_field_id, resource_id, start, end)
        }

        return self.dispatch_request("GET", url, params=jira_search_params)

    def list_issue_change_logs(self, issue_id):
        changelog_url = f'/rest/api/3/issue/{issue_id}/changelog'
        return self.dispatch_request("GET", changelog_url)

    def _generate_jql(self, search_field, resource_id, start, end):
        jql_list = []
        start, end = self.get_start_end_time(start, end)

        if resource_id:
            jql_list.append(f'{search_field} ~ "{resource_id}"')

        if start and end:
            jql_list.append(f'created >= "{start}" AND created <= "{end}"')

        return ' AND '.join(jql_list)
