from spaceone.api.monitoring.plugin import log_pb2, log_pb2_grpc
from spaceone.core.pygrpc import BaseAPI
from cloudforet.monitoring.info.log_info import LogsDataInfo


class Log(BaseAPI, log_pb2_grpc.LogServicer):

    pb2 = log_pb2
    pb2_grpc = log_pb2_grpc

    def list(self, request, context):
        params, metadata = self.parse_request(request, context)

        with self.locator.get_service('LogService', metadata) as log_svc:
            for logs in log_svc.list_logs(params):
                yield self.locator.get_info(LogsDataInfo, logs)
