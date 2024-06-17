import logging

import json_log_formatter
from django.utils import timezone


class CustomisedJSONFormatter(json_log_formatter.JSONFormatter):
    def json_record(self, message: str, extra: dict, record: logging.LogRecord):
        extra['name'] = record.name
        extra['filename'] = record.filename
        extra['funcName'] = record.funcName
        extra['msecs'] = record.msecs
        if record.exc_info:
            extra['exc_info'] = self.formatException(record.exc_info)

        return {
            'message': message,
            'timestamp': timezone.localtime(),
            'level': record.levelname,
            'context': extra
        }
