from logging import getLogger

import requests
from django.conf import settings

from report.telegram import send_error_to_telegram_group

logger = getLogger('backend')


class ApiConnector(object):

    def __new__(cls, *args, **kargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(ApiConnector, cls).__new__(cls)
        return cls._instance

    def __execute(self, method, url, headers, json_payload):
        status_code = 400
        try:
            response = requests.request(method, url, headers=headers, json=json_payload)
            if response.content:
                json_content = None
                try:
                    json_content = response.json()
                except:
                    pass
                return response.status_code, json_content
            status_code = response.status_code
        except Exception as ex:
            logger.error("__execute: Can not execute the call to api", extra=dict(ex=ex))
            message = f'\nFunction: ApiConnector.__execute\nError:\n{ex}'
            send_error_to_telegram_group(message)
        return status_code, None

    def get(self, url, json_payload=None, headers=None):
        # TODO: Add extra code for get if required
        return self.__execute("GET", url, headers, json_payload)

    def post(self, url, json_payload, headers=None):
        # TODO: Add extra code for post if required
        return self.__execute("POST", url, headers, json_payload)

    def put(self, url, json_payload, headers=None):
        # TODO: Add extra code for put if required
        return self.__execute("PUT", url, headers, json_payload)

    def patch(self, url, json_payload, headers=None):
        # TODO: Add extra code for patch if required
        return self.__execute("PATCH", url, headers, json_payload)

    def delete(self, url, json_payload=None, headers=None):
        # TODO: Add extra code for delete if required
        return self.__execute("DELETE", url, headers, json_payload)
