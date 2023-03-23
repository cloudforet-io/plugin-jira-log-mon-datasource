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
                        'options': {
                            'type': 'popup',
                            'layout': {
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
                                            "key": "labels",
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
                        }
                    }
                }),
                TextDyField.data_source('Status', 'status.name'),
                TextDyField.data_source('Project', 'project.name'),
                TextDyField.data_source('Assignee', 'assignee.display_name'),
                TextDyField.data_source('Reporter', 'reporter.display_name'),
                DateTimeDyField.data_source('Created Time', 'created'),
                DateTimeDyField.data_source('Updated Time', 'updated'),
                MoreField.data_source('History', 'change_log_info.name', options={
                    'layout': {
                        'name': 'Activity History',
                        'options': {
                            'type': 'popup',
                            'layout': {
                                'type': 'simple-table',
                                'options': {
                                    'root_path': 'change_log_info.change_logs',
                                    'fields': [
                                        {
                                            "type": "text",
                                            "key": "field",
                                            "name": "Field"
                                        },
                                        {
                                            "type": "text",
                                            "key": "to_string",
                                            "name": "To change"
                                        },
                                        {
                                            "type": "text",
                                            "key": "author.display_name",
                                            "name": "User"
                                        },
                                        {
                                            "type": "datetime",
                                            "source_type": 'iso8601',
                                            "key": "created",
                                            "name": "Changed Time"
                                        }
                                    ]
                                }
                            }
                        }
                    }
                }),
                TextDyField.data_source('Link', 'issue_link.name', options={
                    'link': "{{issue_link.link_url}}"
                })
            ]
        )
        return metadata
