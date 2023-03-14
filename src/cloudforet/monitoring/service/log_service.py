import logging
from spaceone.core.service import *
from cloudforet.monitoring.manager import LogManager

_LOGGER = logging.getLogger(__name__)


@authentication_handler
class LogService(BaseService):
    def __init__(self, metadata):
        super().__init__(metadata)

    @transaction
    @check_required(['options', 'secret_data', 'query', 'start', 'end'])
    @change_timestamp_value(['start', 'end'], timestamp_format='iso8601')
    def list_logs(self, params):
        """ Get quick list of resources

        Args:
            params (dict) {
                'options': 'dict',
                'schema': 'str',
                'secret_data': 'dict',
                'query': 'dict',
                'keyword': 'str',
                'start': 'timestamp',
                'end': 'timestamp',
                'sort': 'dict',
                'limit': 'int'
            }

        Returns: list of resources
        """
        log_manager = self.locator.get_manager(LogManager)
        for logs in log_manager.list_logs(params):
            yield logs
