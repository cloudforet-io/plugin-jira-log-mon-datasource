from schematics import Model
from schematics.types import ModelType, StringType, DateTimeType, ListType, BooleanType, IntType


class JiraAccount(Model):
    account_id = StringType(serialize_when_none=False, deserialize_from="accountId")
    account_type = StringType(serialize_when_none=False, deserialize_from="accountType")
    active = BooleanType(serialize_when_none=False)
    display_name = StringType(serialize_when_none=False, deserialize_from="displayName")
    self = StringType(serialize_when_none=False)
    time_zone = StringType(serialize_when_none=False, deserialize_from="timeZone")


class IssueAssignee(JiraAccount):
    pass


class IssueCreator(JiraAccount):
    pass


class IssueReporter(JiraAccount):
    email_address = StringType(serialize_when_none=False, deserialize_from="emailAddress")


class IssueProgress(Model):
    progress = IntType(serialize_when_none=False)
    total = IntType(serialize_when_none=False)


class JiraProject(Model):
    id = StringType(serialize_when_none=False)
    key = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    project_type_key = StringType(serialize_when_none=False, deserialize_from="projectTypeKey")
    self = StringType(serialize_when_none=False)


class IssueResolution(Model):
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    self = StringType(serialize_when_none=False)
    description = StringType(serialize_when_none=False)


class IssueStatusCategory(Model):
    color_name = StringType(serialize_when_none=False, deserialize_from="colorName")
    id = StringType(serialize_when_none=False)
    key = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    self = StringType(serialize_when_none=False)


class IssueStatus(Model):
    description = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    self = StringType(serialize_when_none=False)
    status_category = ModelType(IssueStatusCategory, serialize_when_none=False, deserialize_from="statusCategory")


class IssuePriority(Model):
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    self = StringType(serialize_when_none=False)


class IssueRequestType(Model):
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    description = StringType(serialize_when_none=False)
    self = StringType(serialize_when_none=False)
    issue_type_id = StringType(serialize_when_none=False)
    service_desk_id = StringType(serialize_when_none=False)
    portal_id = StringType(serialize_when_none=False)


class IssueChangeLog(Model):
    id = StringType(serialize_when_none=False)
    author = ModelType(JiraAccount)
    created = DateTimeType(serialize_when_none=False)
    field = StringType(default=None)
    from_string = StringType(default=None)
    to_string = StringType(default=None)


class IssueHistory(Model):
    name = StringType(default='View')
    change_logs = ListType(ModelType(IssueChangeLog), default=[])


class IssueLink(Model):
    name = StringType(default='Link')
    link_url = StringType(default='')


class JIRAIssueInfo(Model):
    title = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    status = ModelType(IssueStatus, serialize_when_none=False)
    status_category_change_date = DateTimeType(serialize_when_none=False)
    key = StringType(serialize_when_none=False)
    self = StringType(serialize_when_none=False)
    project = ModelType(JiraProject, default={})
    reporter = ModelType(IssueReporter, default={})
    creator = ModelType(IssueCreator, default={})
    assignee = ModelType(IssueAssignee, default={})
    progress = ModelType(IssueProgress)
    priority = ModelType(IssuePriority, default={})
    request_type = ModelType(IssueRequestType, default={})
    resolution = ModelType(IssueResolution, default={})
    resolution_date = DateTimeType(serialize_when_none=False)
    description = StringType(serialize_when_none=False)
    duedate = DateTimeType(serialize_when_none=False)
    environment = StringType(serialize_when_none=False)
    labels = ListType(StringType(serialize_when_none=False), default=[])
    change_log_info = ModelType(IssueHistory)
    issue_link = ModelType(IssueLink)
    created = DateTimeType(serialize_when_none=False)
    updated = DateTimeType(serialize_when_none=False)


class Log(Model):
    results = ListType(ModelType(JIRAIssueInfo), default=[])
