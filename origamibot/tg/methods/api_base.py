import json
from typing import Union
from abc import ABC

from gevent import sleep
from genki import post, Response
from genki.http.exceptions import network_exceptions
from genki.http.url import URL
from flowerfield import Scheme

from .util import DEFAULT_API_SERVER, addr
from ..exceptions import TelegramAPIError


class APIBase(ABC):
    """Base class that implements basic methods to send requests
    to TelegramAPI
    """

    def url_for(self, method: str) -> str:
        """Returns url for given method
        """
        return f"{str(self.host)}bot{self.token}/{method}"

    def _unwrap_result(self, responce: Response) -> Union[dict, list]:
        is_ok = False
        result = None

        json_obj = json.loads(responce.body)
        assert isinstance(json_obj, dict)
        assert "ok" in json_obj

        if json_obj["ok"]:
            is_ok = True
            result = json_obj["result"]
        else:
            is_ok = False
            result = json_obj["description"]

        if is_ok:
            return result
        else:
            raise TelegramAPIError(f"[{responce.status_code}] {result}")

    def _send_request(self, method: str, data: dict = {}, files: dict = {}) -> Response:
        """Sends request to server, returns Reponce object"""
        timeout = data.get('timeout')
        if timeout is not None:
            timeout += 2
        if files:
            raise NotImplementedError("Sending files is not supported yet.")

        retries = self.max_retries
        result = post(self.url_for(method), data=data, timeout=timeout).result()

        while isinstance(result, network_exceptions) and retries > 0:
            sleep()
            retries -= 1
            result = post(self.url_for(method), data=data, timeout=timeout).result()

        if isinstance(result, network_exceptions):
            raise result

        return result

    def _purify_data(self, data: dict) -> dict:
        """Returns dict with no None fields
        and removes self from it, usually used with locals() in methods
        """
        return {
            key: (self._purify_data(value)
                  if isinstance(value, dict)
                  else value.as_dict()
                  if isinstance(value, Scheme)
                  else value)
            for key, value in data.items()
            if value is not None and key != "self"
        }

    def _simple_request(self, method: str, data: dict) -> Union[dict, list]:
        """Helper method for simple requests
        sends data dict and returns result field from server.
        """
        data = self._purify_data(data)
        responce = self._send_request(method, data)
        return self._unwrap_result(responce)

    def __init__(self, token: str, host: addr = DEFAULT_API_SERVER, request_retries=5):
        self.token = token

        assert isinstance(host, (str, URL))
        if isinstance(host, str):
            self.host = URL(host)
        else:
            self.host = host

        self.max_retries = request_retries