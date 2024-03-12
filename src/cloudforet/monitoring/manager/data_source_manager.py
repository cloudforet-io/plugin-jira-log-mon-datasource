import logging
from spaceone.core.manager import BaseManager
from cloudforet.monitoring.connector.jira import JiraConnector
from cloudforet.monitoring.model.data_source_response_model import DataSourceMetadata
from cloudforet.monitoring.manager.metadata_manager import MetadataManager

_LOGGER = logging.getLogger(__name__)


class DataSourceManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def init(params):
        options = params['options']
        meta_manager = MetadataManager()
        response_model = DataSourceMetadata({'_metadata': meta_manager.get_data_source_metadata()}, strict=False)
        return response_model.to_primitive()

    def verify(self, params):
        self.locator.get_connector(JiraConnector, **params)
