import logging
import datetime
import requests
from requests.auth import HTTPBasicAuth
from typing import Union, Generator

from spaceone.core.error import *
from spaceone.core.connector import BaseConnector

__all__ = ["JiraBaseConnector"]

_LOGGER = logging.getLogger(__name__)


class JiraBaseConnector(BaseConnector):
    cloud_service_type = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.secret_data = kwargs.get("secret_data", {})
        self.project_key = self.secret_data.get("project_key")

    def dispatch_request(
            self,
            method: str,
            url: str,
            data: dict = None,
            params: dict = None,
    ) -> Union[Generator[dict, None, None], list]:
        # Set up request
        url = f"{self.get_base_url()}{url}"
        headers = {"Accept": "application/json"}
        auth = self.get_auth()

        try:
            for response in self._pagination(method, url, headers, auth, params, data):
                yield response

        except Exception as e:
            _LOGGER.error(f"[dispatch_request] Error {e}")
            raise ERROR_UNKNOWN(message=e)

    @staticmethod
    def _pagination(
            method: str,
            url: str,
            headers: dict,
            auth: HTTPBasicAuth,
            params: dict,
            data: dict = None,
    ) -> list:
        responses = []
        while True:
            response = requests.request(
                method,
                url,
                headers=headers,
                auth=auth,
                params=params,
                json=data,
            )
            response_json = response.json()
            if isinstance(response_json, list):
                response_values = response_json
            else:
                response_values = response_json.get("values")

            _LOGGER.debug(
                f"[dispatch_request] {url} {response.status_code} {response.reason}"
            )

            if response.status_code != 200:
                raise ERROR_UNKNOWN(
                    message=f"Error {response.status_code} {response.text}"
                )

            if response_values:
                responses.extend(response_values)
            else:
                responses.append(response_json)

            if (
                    isinstance(response_json, list)
                    or response_json.get("isLast", True)
                    or response_json.get("isLast") is None
            ):
                break
            else:
                url = response_json.get("nextPage")
        return responses

    def get_base_url(self) -> str:
        domain = self.secret_data.get("domain")
        return f"https://{domain}.atlassian.net/"

    def get_auth(self) -> HTTPBasicAuth:
        email = self.secret_data.get("email")
        api_token = self.secret_data.get("api_token")
        return HTTPBasicAuth(username=email, password=api_token)

    @staticmethod
    def get_start_end_time(start, end):
        try:
            _start = start.strftime('%Y/%m/%d')
            end = end + datetime.timedelta(days=1)
            _end = end.strftime('%Y/%m/%d')
            return _start, _end

        except Exception as e:
            print(e)
            return None, None
