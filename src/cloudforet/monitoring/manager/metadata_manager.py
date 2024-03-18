import logging
from spaceone.core.manager import BaseManager
from cloudforet.monitoring.model.metadata.metadata import LogMetadata
from cloudforet.monitoring.model.metadata.metadata_dynamic_field import TextDyField, DateTimeDyField, ListDyField, \
    MoreField

_LOGGER = logging.getLogger(__name__)


class MetadataManager(BaseManager):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def get_data_source_metadata(options):
        if options.get("custom_fields"):
            metadata = LogMetadata.set_fields(
                name='jira-issue-table',
                fields=[
                    TextDyField.data_source('Issue Type', 'issue_type'),
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
                                        ]
                                    }
                                }
                            }
                        }
                    }),
                    TextDyField.data_source('Status', 'status.name'),
                    TextDyField.data_source('Project', 'project.name', options={'link': 'issue_link.link_url'}),
                    TextDyField.data_source('Assignee', 'assignee.display_name'),
                    TextDyField.data_source('Reporter', 'reporter.display_name'),
                    ListDyField.data_source('Approvers', 'custom.approvers', options={'delimiter': "<br>"}),
                    DateTimeDyField.data_source('Approval Time', 'custom.approval_time'),
                    DateTimeDyField.data_source('Created Time', 'created'),
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
                    })
                ]
            )
        else:
            metadata = LogMetadata.set_fields(
                name='jira-issue-table',
                fields=[
                    TextDyField.data_source('Issue Type', 'status.name'),
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
                                        ]
                                    }
                                }
                            }
                        }
                    }),
                    TextDyField.data_source('Status', 'status.name'),
                    TextDyField.data_source('Priority', 'priority.name'),
                    TextDyField.data_source('Project', 'project.name', options={'link': 'issue_link.link_url'}),
                    TextDyField.data_source('Assignee', 'assignee.display_name'),
                    TextDyField.data_source('Reporter', 'reporter.display_name'),
                    DateTimeDyField.data_source('Created Time', 'created'),
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
                    })
                ]
            )
        return metadata
