import logging
from spaceone.core.manager import BaseManager
from cloudforet.monitoring.model.metadata.metadata import LogMetadata
from cloudforet.monitoring.model.metadata.metadata_dynamic_field import TextDyField, DateTimeDyField, ListDyField, \
    MoreField
from cloudforet.monitoring.conf.monitoring_conf import *

_LOGGER = logging.getLogger(__name__)


class MetadataManager(BaseManager):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def get_data_source_metadata():
        metadata = LogMetadata.set_fields(
            name='jira-issue-table',
            fields=[
                MoreField.data_source('Title', 'title', options={
                    'layout': {
                        'name': 'Issue Information',
                        'type': 'item',
                        'options': {
                            'fields': [
                                {
                                    "type": "text",
                                    "key": "title",
                                    "name": "Title"
                                },
                                {
                                    "type": "text",
                                    "key": "key",
                                    "name": "Key"
                                },
                                {
                                    "type": "text",
                                    "key": "description",
                                    "name": "Description"
                                },
                                {
                                    "type": "text",
                                    "key": "priority.name",
                                    "name": "Priority"
                                },
                                {
                                    "type": "text",
                                    "key": "assignee.display_name",
                                    "name": "Assignee"
                                },
                                {
                                    "type": "text",
                                    "key": "reporter.display_name",
                                    "name": "Reporter"
                                },
                                {
                                    "type": "list",
                                    "key": "reporter.display_name",
                                    "name": "Labels",
                                    "options": {
                                        "delimiter": "<br>",
                                        "item": {
                                            "type": "badge",
                                            "options": {
                                                "outline_color": "violet.500"
                                            }
                                        }
                                    }
                                }
                            ]
                        }
                    }
                }),
                TextDyField.data_source('Status', 'status.name'),
                TextDyField.data_source('Project', 'project.name'),
                TextDyField.data_source('Assignee', 'assignee.display_name'),
                TextDyField.data_source('Reporter', 'reporter.display_name'),
                DateTimeDyField.data_source('Created Time', 'created'),
                DateTimeDyField.data_source('Updated Time', 'updated'),
            ]
        )
        return metadata
