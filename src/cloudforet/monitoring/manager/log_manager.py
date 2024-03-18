import logging
from datetime import datetime
from spaceone.core.manager import BaseManager
from cloudforet.monitoring.connector.jira import JiraConnector
from cloudforet.monitoring.model.log_model import Log, JIRAIssueInfo

_LOGGER = logging.getLogger(__name__)


class LogManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def list_logs(self, params):
        query = params.get('query')
        resource_id = query.get('resource_id')
        start = params.get('start')
        end = params.get('end')
        options = params.get('options', {})
        field_name = options.get('search_field', 'resource_id')
        secret_data = params.get('secret_data', {})

        results = []
        jira_connector = self.locator.get_connector(JiraConnector, **params)
        issues_generator = jira_connector.list_issues(field_name, resource_id, start, end)
        issues_info = [issues_info for issues_info in issues_generator]
        for issue_info in issues_info:
            for issue in issue_info["issues"]:
                issue_dict = {
                    'id': issue.get('id'),
                    'key': issue.get('key'),
                    'self': issue.get('self'),
                    'issue_link': {'link_url': self._generate_jira_link_url(secret_data, issue.get('key'))}
                }

                _issue_field = issue.get('fields', {})
                issue_dict.update({
                    'issue_type': _issue_field.get('issuetype').get('name', 'Unknown'),
                    'title': _issue_field.get('summary'),
                    'project': _issue_field.get('project', {}),
                    'status': _issue_field.get('status'),
                    'status_category_change_date': _issue_field.get('statuscategorychangedate'),
                    'reporter': _issue_field.get('reporter'),
                    'creator': _issue_field.get('creator'),
                    'progress': _issue_field.get('progress'),
                    'duedate': self.convert_datetime(_issue_field.get('duedate')),
                    'priority': _issue_field.get('priority'),
                    'environment': _issue_field.get('environment'),
                    'assignee': _issue_field.get('assignee'),
                    'resolution': _issue_field.get('resolution'),
                    'resolution_date': _issue_field.get('resolutiondate'),
                    'description': self._get_description(_issue_field.get('description')),
                    'labels': _issue_field.get('labels', []),
                    'created': _issue_field.get('created'),
                    'updated': _issue_field.get('updated'),
                    'change_log_info': {'change_logs': self._get_change_logs(jira_connector, issue.get('id'))}
                })

                # Temp code
                if custom_fields := options.get("custom_fields"):
                    for key, value in custom_fields.items():
                        if isinstance(_issue_field[value], list):
                            approvers_info = _issue_field[value]
                            approvers = []

                            for approver_info in approvers_info:
                                approvers.append(approver_info["displayName"])

                            _issue_field[value] = approvers

                        if "custom" in issue_dict:
                            issue_dict["custom"].update({key: _issue_field.get(value)})
                        else:
                            issue_dict["custom"] = {key: _issue_field.get(value)}
                results.append(JIRAIssueInfo(issue_dict, strict=False))

        yield Log({'results': results})

    def _get_change_logs(self, jira_connector, issue_id):
        _logs = jira_connector.list_issue_change_logs(issue_id)
        return [self._set_change_log(_log) for _log in _logs]

    @staticmethod
    def _set_change_log(log):
        log_dict = {
            'id': log.get('id'),
            'created': log.get('created'),
            'author': log.get('author')
        }

        if log.get('items'):
            _item = log.get('items')[0]
            log_dict.update({
                'field': _item.get('field'),
                'from_string': _item.get('fromString'),
                'to_string': _item.get('toString')
            })

        return log_dict

    @staticmethod
    def _get_description(jira_description):
        description = ''

        if jira_description:
            contents = jira_description.get('content', [])

            for _content in contents:
                for _info in _content.get('content', []):
                    description += _info.get('text', '')

        return description

    @staticmethod
    def convert_datetime(date):
        if date:
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            return date_obj.timestamp()

        return None

    @staticmethod
    def _generate_jira_link_url(secret_data, key):
        return f'{secret_data.get("url", "")}/browse/{key}'
