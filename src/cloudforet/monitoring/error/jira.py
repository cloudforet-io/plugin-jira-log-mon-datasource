from spaceone.core.error import *


class ERROR_INVALID_JIRA_CREDENTIAL(ERROR_INVALID_ARGUMENT):
    _message = 'Jira credentials is invalid.(url={url} email={email} api_token={api_token})'
